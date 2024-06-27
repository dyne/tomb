/**
 * Copyright (c) 2013 Dmitriy Scherbina
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is furnished
 * to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

/**
 * Javascript email protection (JEP).
 * Perfectly protects your email from bots that are scanning HTML without executing JavaScript.
 *
 * Usage in HTML:
 *
 *  <script type="text/javascript">jep_link("example.com", "mailbox");</script>
 *  => writes to DOM: <a href="mailto:mailbox@example.com">mail@example.com</a>
 *
 *  <script type="text/javascript">jep_link("example.com", "mailbox", "my email");</script>
 *  => writes to DOM: <a href="mailto:mailbox@example.com">my email</a>
 *
 *  <script type="text/javascript">jep_link("example.com", "mailbox", "my email", true);</script>
 *  => returns as string: <a href="mailto:mailbox@example.com">my email</a>
 *
 * @param domain: string, domain address. Ex.: example.com
 * @param email: string, email address at domain. Ex.: mailbox
 * @param text: string, text that link will have (optional, default: email address wil be used as text)
 * @param returnHtml: boolean, print or return generated HTML (optional, default: false)
 */
 function jep_link(domain, email, text, returnHtml) {
  var url = email + '@' + domain;
  var link = '<a class="_button" href="ma' + 'i' + 'lto:' + url + '">' + (text ? text : url) + '</a>';

  if (returnHtml) {
      return link;
  } else {
      document.write(link);
  }
}
