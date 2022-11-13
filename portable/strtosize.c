/* strtosize from util-linux */

/* No copyright is claimed.  This code is in the public domain. */

#include <ctype.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <locale.h>
#include <inttypes.h>

static int do_scale_by_power (uintmax_t *x, int base, int power)
{
	while (power--) {
		if (UINTMAX_MAX / base < *x)
			return -ERANGE;
		*x *= base;
	}
	return 0;
}

/*
 * strtosize() - convert string to size (uintmax_t).
 *
 * Supported suffixes:
 *
 * XiB or X for 2^N
 *     where X = {K,M,G,T,P,E,Z,Y}
 *        or X = {k,m,g,t,p,e}  (undocumented for backward compatibility only)
 * for example:
 *		10KiB	= 10240
 *		10K	= 10240
 *
 * XB for 10^N
 *     where X = {K,M,G,T,P,E,Z,Y}
 * for example:
 *		10KB	= 10000
 *
 * The optional 'power' variable returns number associated with used suffix
 * {K,M,G,T,P,E,Z,Y}  = {1,2,3,4,5,6,7,8}.
 *
 * The function also supports decimal point, for example:
 *              0.5MB   = 500000
 *              0.5MiB  = 512000
 *
 * Note that the function does not accept numbers with '-' (negative sign)
 * prefix.
 */
int strtosize(const char *str, uintmax_t *res, int *power)
{
	const char *p;
	char *end;
	uintmax_t x, frac = 0;
	int base = 1024, rc = 0, pwr = 0, frac_zeros = 0;

	static const char *suf  = "KMGTPEZY";
	static const char *suf2 = "kmgtpezy";
	const char *sp;

	*res = 0;

	if (!str || !*str) {
		rc = -EINVAL;
		goto err;
	}

	/* Only positive numbers are acceptable
	 *
	 * Note that this check is not perfect, it would be better to
	 * use lconv->negative_sign. But coreutils use the same solution,
	 * so it's probably good enough...
	 */
	p = str;
	while (isspace((unsigned char) *p))
		p++;
	if (*p == '-') {
		rc = -EINVAL;
		goto err;
	}

	errno = 0, end = NULL;
	x = strtoumax(str, &end, 0);

	if (end == str ||
	    (errno != 0 && (x == UINTMAX_MAX || x == 0))) {
		rc = errno ? -errno : -EINVAL;
		goto err;
	}
	if (!end || !*end)
		goto done;			/* without suffix */
	p = end;

	/*
	 * Check size suffixes
	 */
check_suffix:
	if (*(p + 1) == 'i' && (*(p + 2) == 'B' || *(p + 2) == 'b') && !*(p + 3))
		base = 1024;			/* XiB, 2^N */
	else if ((*(p + 1) == 'B' || *(p + 1) == 'b') && !*(p + 2))
		base = 1000;			/* XB, 10^N */
	else if (*(p + 1)) {
		struct lconv const *l = localeconv();
		const char *dp = l ? l->decimal_point : NULL;
		size_t dpsz = dp ? strlen(dp) : 0;

		if (frac == 0 && *p && dp && strncmp(dp, p, dpsz) == 0) {
			const char *fstr = p + dpsz;

			for (p = fstr; *p == '0'; p++)
				frac_zeros++;
			fstr = p;
			if (isdigit(*fstr)) {
				errno = 0, end = NULL;
				frac = strtoumax(fstr, &end, 0);
				if (end == fstr ||
				    (errno != 0 && (frac == UINTMAX_MAX || frac == 0))) {
					rc = errno ? -errno : -EINVAL;
					goto err;
				}
			} else
				end = (char *) p;

			if (frac && (!end  || !*end)) {
				rc = -EINVAL;
				goto err;		/* without suffix, but with frac */
			}
			p = end;
			goto check_suffix;
		}
		rc = -EINVAL;
		goto err;			/* unexpected suffix */
	}

	sp = strchr(suf, *p);
	if (sp)
		pwr = (sp - suf) + 1;
	else {
		sp = strchr(suf2, *p);
		if (sp)
			pwr = (sp - suf2) + 1;
		else {
			rc = -EINVAL;
			goto err;
		}
	}

	rc = do_scale_by_power(&x, base, pwr);
	if (power)
		*power = pwr;
	if (frac && pwr) {
		int i;
		uintmax_t frac_div = 10, frac_poz = 1, frac_base = 1;

		/* mega, giga, ... */
		do_scale_by_power(&frac_base, base, pwr);

		/* maximal divisor for last digit (e.g. for 0.05 is
		 * frac_div=100, for 0.054 is frac_div=1000, etc.)
		 *
		 * Reduce frac if too large.
		 */
		while (frac_div < frac) {
			if (frac_div <= UINTMAX_MAX/10)
				frac_div *= 10;
			else
				frac /= 10;
		}

		/* 'frac' is without zeros (5 means 0.5 as well as 0.05) */
		for (i = 0; i < frac_zeros; i++) {
			if (frac_div <= UINTMAX_MAX/10)
				frac_div *= 10;
			else
				frac /= 10;
		}

		/*
		 * Go backwardly from last digit and add to result what the
		 * digit represents in the frac_base. For example 0.25G
		 *
		 *  5 means 1GiB / (100/5)
		 *  2 means 1GiB / (10/2)
		 */
		do {
			unsigned int seg = frac % 10;		 /* last digit of the frac */
			uintmax_t seg_div = frac_div / frac_poz; /* what represents the segment 1000, 100, .. */

			frac /= 10;	/* remove last digit from frac */
			frac_poz *= 10;

			if (seg && seg_div / seg)
				x += frac_base / (seg_div / seg);
		} while (frac);
	}
done:
	*res = x;
err:
	if (rc < 0)
		errno = -rc;
	return rc;
}

int main(int argc, char **argv) {
  // TODO: secure check args
  uint64_t size;
  if(argc!=2) return(1);
  int res = strtosize(argv[1], &size, NULL);
  if(res==0) {
	fprintf(stdout,"%lu\n",size);
  } else {
	fprintf(stderr,"%s\n",strerror(errno));
  }
  return(res);
}
