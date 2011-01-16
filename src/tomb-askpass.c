/* Tomb askpass
   
   Derived from gtk-led-askpass.c version 0.9
   by Dafydd Harries <daf@muse.19inch.net>, 2003 2004
   (An ssh-askpass alike software)
   
   Based on ideas from ssh-askpass-gnome, by Damien Miller and Nalin Dahyabhai,
   and on Jim Knoble's x11-ssh-askpass.
   
   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.
   
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
   
   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software Foundation, Inc.,
   59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
   
   See also:
   
   http://www.cgabriel.org/sw/gtk2-ssh-askpass/
   -- Jim Knoble's x11-ssh-askpass
   http://www.cgabriel.org/sw/gtk2-ssh-askpass/
   -- Christopher Gabriel's gtk2-ssh-askpass
   
   Todo:

   - Internationalise. Probably entails autotoolising.
   - Add more eye candy.
   - Implement optional mouse/server grabbing.
   - Alow overriding the title on the command line.
   - Make the LED box a proper GTK+ widget.
   
*/

#include <gdk/gdk.h>
#include <gtk/gtk.h>
#include <gdk/gdkkeysyms.h>

/* The Tomb icon is an artwork by Jordi aka MonMort
   a nomadic graffiti artist from Barcelona */
#include <monmort.xpm>

/* Title for the dialog. */
#define TITLE "Unlocking tomb"

/* Width of each LED. */
#define LED_WIDTH 8
/* Height of each LED. */
#define LED_HEIGHT 16
/* Space around and between LEDs. */
#define LED_MARGIN 5
/* Number of LEDs to have. */
#define LED_COUNT 12

/* How many times to attempt to grab the keyboard before giving up. */
#define GRAB_TRIES_MAX 10
/* How long to sleep, in microseconds, in between keyboard grab attempts. */
#define GRAB_SLEEP 100000
/* Sleep length, in milliseconds, after Control-U press. */
#define CLEAR_SLEEP 800

enum {
	LED_STATE_OFF,
	LED_STATE_GREEN,
	LED_STATE_RED,
	LED_STATES
};

GdkPixbuf *pb_monmort;

GdkColor colours[LED_STATES] = {
	/* LED_STATE_OFF */
	{ 0, 0x3333, 0x6666, 0x3333 },
	/* LED_STATE_GREEN */
	{ 0, 0x6666, 0xFFFF, 0x6666 },
	/* LED_STATE_RED */
	{ 0, 0xDDDD, 0x3333, 0x3333 }
};


void draw_led(GtkWidget *widget, gint state, guint offset)
{
	GdkGC *gc = gdk_gc_new(widget->window);

	/* Draw the border. */
	gdk_draw_rectangle(widget->window,
		widget->style->fg_gc[GTK_WIDGET_STATE(widget)],
		FALSE,
		LED_MARGIN + offset * (LED_WIDTH + LED_MARGIN),
		LED_MARGIN,
		LED_WIDTH,
		LED_HEIGHT);

	gdk_gc_set_rgb_fg_color(gc, &(colours[state]));

	/* Draw the inside rectangle. */
	gdk_draw_rectangle(widget->window,
		gc,
		TRUE,
		LED_MARGIN + offset * (LED_WIDTH + LED_MARGIN) + 1,
		LED_MARGIN + 1,
		LED_WIDTH - 1,
		LED_HEIGHT - 1);
}

gboolean led_area_expose_handler(GtkWidget *led_area, GdkEventExpose *event,
	GString *passphrase)
{
	gint i, width, height;
	gint length = passphrase->len;

	gdk_drawable_get_size(GDK_DRAWABLE(led_area->window), &width, &height);

	/* Draw a focus indicator if appropriate. */
	if (GTK_WIDGET_HAS_FOCUS(led_area))
		gtk_paint_focus(led_area->style, led_area->window,
			GTK_WIDGET_STATE(led_area), &(event->area), led_area,
			"", 0, 0, width, height);

	/* Draw each LED. */
	for (i = 0; i < LED_COUNT; i++) {
		/* This is the complicated bit. */
		gboolean on = ((length / LED_COUNT) % 2 == 0) ?
				(length % LED_COUNT >  i) :
				(length % LED_COUNT <= i);

		draw_led(led_area, on ? LED_STATE_GREEN : LED_STATE_OFF, i);
	}

	/* TRUE means not to propagate the event. */
	return TRUE;
}

gboolean timeout_handler(GtkWidget *led_area)
{
	gtk_widget_queue_draw(led_area);

	return FALSE;
}

void clear(GString *passphrase, GtkWidget *led_area)
{
	gint i;

	/*
	Delete bit by bit to ensure erasure. g_string_erase() will overwrite
	the last character with 0, so we shouldn't need to worry about leaving
	sensitive data in memory. Note that the string may be empty. This is
	so that the interface responds consistently.
	*/
	while (passphrase->len > 0)
		g_string_erase(passphrase, passphrase->len - 1, 1);

	for (i = 0; i < LED_COUNT; i++)
		draw_led(led_area, LED_STATE_RED, i);

	/*
	Remove the redness after a delay. If an exposure is triggered, such as
	by a key getting pressed, then the redraw will simply happen early.
	*/
	gtk_timeout_add(CLEAR_SLEEP, (GtkFunction)timeout_handler, led_area);
}

gboolean led_area_key_press_handler(GtkWidget *led_area, GdkEventKey *event,
				    GString *passphrase) {
  /* Obtain Unicode representation of key released. */
  gunichar c = gdk_keyval_to_unicode(event->keyval);
  /* Determine whether the key released was printable. */
  gint isprint = g_unichar_isprint(c);
  /* Obtain default modifier mask. */
  guint modifiers = gtk_accelerator_get_default_mod_mask();
  
  if (event->keyval == GDK_Delete) {
    clear(passphrase, led_area);
    return TRUE;
  }

  if ((event->state & modifiers) == GDK_CONTROL_MASK) {

    if (event->keyval == GDK_u) {
      /* C-u -- delete everything. */
      clear(passphrase, led_area);
      /* Return early in order to avoid the redraw. */
      return TRUE;

    } else {

      /* Unrecognised keypress. */
      return FALSE;
    }
    
  } else if (event->keyval == GDK_BackSpace && passphrase->len > 0) {
    /*
      Backspace -- remove last character. See the comment above
      about g_string_erase.
    */
    g_string_erase(passphrase, passphrase->len - 1, 1);
	} else if (isprint) {
		/* Printable character. */
		g_string_append_unichar(passphrase, c);
	} else {
		/* Unrecognized keypress, propagate. */
		return FALSE;
	}

	/* Trigger a redraw of the LED area. */
	gtk_widget_queue_draw(led_area);

	/* TRUE means not to propagate the event. */
	return TRUE;
}

gboolean led_area_button_press_handler(GtkWidget *led_area,
	GdkEventButton *event, gpointer data)
{
	gtk_widget_grab_focus(led_area);

	return TRUE;
}

int main(int argc, char *argv[])
{
	gint response, grab_tries, i;
	char keyname[256];
	GString *passphrase = g_string_new("");
	GtkWidget *dialog, *alignment, *led_area;
	GList tmplist;

	gtk_set_locale();
	gtk_init(&argc, &argv);

	if (argc > 1) {
	  snprintf(keyname,255,"%s",argv[1]);
	} else {
	  sprintf(keyname,"unknown");
	}
	/*
	dialog
	`- vbox (implicit)
	   `- aligment
	      `- led_area
	*/

	/* Question dialog with no parent; OK and Cancel buttons. */
	dialog = gtk_message_dialog_new_with_markup
	  (NULL, 0, GTK_MESSAGE_QUESTION, GTK_BUTTONS_OK,
	   "Enter the password to unlock\n"
	   "<span font=\"Times 24\">%s</span>", keyname);
	gtk_window_set_title(GTK_WINDOW(dialog), TITLE);

	// set and show the image icon
	pb_monmort = gdk_pixbuf_new_from_xpm_data(monmort);
	tmplist.data = (gpointer*)pb_monmort;
	tmplist.prev = tmplist.next = NULL;
	gtk_window_set_icon_list(GTK_WINDOW(dialog), &tmplist);
	gtk_message_dialog_set_image(GTK_MESSAGE_DIALOG(dialog), 
				     gtk_image_new_from_pixbuf(pb_monmort));

	/* Place the dialog in the middle of the screen. */
	gtk_window_set_position(GTK_WINDOW(dialog), GTK_WIN_POS_CENTER);
	/* OK is the default action. */
	gtk_dialog_set_default_response(GTK_DIALOG(dialog), GTK_RESPONSE_OK);
	
	/* Add some spacing within the dialog's vbox. */
	gtk_box_set_spacing(GTK_BOX(GTK_DIALOG(dialog)->vbox), 3);

	/* The alignment widget containing the drawing area. */
	alignment = gtk_alignment_new(0.5, 0.5, 0, 0);
	gtk_container_add(GTK_CONTAINER(GTK_DIALOG(dialog)->vbox), alignment);

	/* The drawing area for the LEDs. */
	led_area = gtk_drawing_area_new();
	gtk_container_add(GTK_CONTAINER(alignment), led_area);
	/* Make the LED widget focusable. */
	GTK_WIDGET_SET_FLAGS(led_area, GTK_CAN_FOCUS);
	/* Make the LED widget focused. */
	gtk_widget_grab_focus(led_area);
	/* Make the LED widget receive key press and button press events. */
	gtk_widget_add_events(led_area,
		GDK_KEY_PRESS_MASK | GDK_BUTTON_PRESS_MASK);
	/* Set a size request. */
	gtk_widget_set_size_request(led_area,
		LED_MARGIN + (LED_WIDTH + LED_MARGIN) * LED_COUNT,
		LED_HEIGHT + LED_MARGIN * 2);
	/* Set up handler for key releases. */
	g_signal_connect(G_OBJECT(led_area), "key_press_event",
		G_CALLBACK(led_area_key_press_handler), passphrase);
	/* Set up handler for button releases. */
	g_signal_connect(G_OBJECT(led_area), "button_press_event",
		G_CALLBACK(led_area_button_press_handler), NULL);
	/* Set up handler for expose events. */
	g_signal_connect(G_OBJECT(led_area), "expose_event",
		G_CALLBACK(led_area_expose_handler), passphrase);

	
	/* Show all the widgets. */
	gtk_widget_show_all(dialog);
	/* Put the dialog on the screen now for the grab to work. */
	gtk_widget_show_now(dialog);

	/* Grab the keyboard */
	gdk_keyboard_grab(GTK_WIDGET(dialog)->window, FALSE, GDK_CURRENT_TIME);
	
	/* Make the dialog stay on top. */
	gtk_window_set_keep_above(GTK_WINDOW(dialog), TRUE);

	/* Run the dialog. */
	response = gtk_dialog_run(GTK_DIALOG(dialog));

	/* Ungrab the keyboard. */
	gdk_keyboard_ungrab(GDK_CURRENT_TIME);

	/* If the OK button was pressed, print the passphrase. */
	if (response == GTK_RESPONSE_OK)
		g_print("%s\n", passphrase->str);

	/* Scrub the passphrase, if any. */
	for (i = 0; i < passphrase->len; i++)
		passphrase->str[i] = '\0';

	if (response == GTK_RESPONSE_OK)
		return 0;

	return 1;
}

