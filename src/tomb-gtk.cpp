/*  Tomb - encrypted storage undertaker
 *  
 *  (c) Copyright 2007-2011 Denis Roio <jaromil@dyne.org>
 *
 * This source code is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Public License as published 
 * by the Free Software Foundation; either version 3 of the License,
 * or (at your option) any later version.
 *
 * This source code is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * Please refer to the GNU Public License for more details.
 *
 * You should have received a copy of the GNU Public License along with
 * this source code; if not, write to:
 * Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include <gtk/gtk.h>
#include <libnotify/notify.h>

/* The Tomb icon is an artwork by Jordi aka MonMort
   a nomadic graffiti artist from Barcelona */
#include <monmort.xpm>

GtkStatusIcon *status_tomb;
GtkMenu *menu_tomb;

NotifyNotification *notice;
GError *error;

// forward declaration of callbacks
gboolean left_click(GtkWidget *w, GdkEvent *e);
gboolean cb_close(GtkWidget *w, GdkEvent *e);


int main(int argc, char **argv) {
  GObject *tray;
  GdkPixbuf *pb_monmort;
  GtkWidget *menu_close;
  gint menu_x, menu_y;
  gboolean push_in = true;

  char tomb_file[512];
  
  gtk_set_locale();
  gtk_init(&argc, &argv);

  // libnotify
  notify_init(PACKAGE);

  // set and show the status icon
  pb_monmort = gdk_pixbuf_new_from_xpm_data(monmort);
  status_tomb = gtk_status_icon_new_from_pixbuf(pb_monmort);
  //  gtk_status_icon_set_name(status_tomb, "tomb");
  gtk_status_icon_set_title(status_tomb, "Tomb");
  gtk_status_icon_set_tooltip_text (status_tomb, "Tomb - crypto undertaker");

  //  gtk_status_icon_set_blinking(status_tomb, true);
  menu_tomb = (GtkMenu*) gtk_menu_new();

  menu_close = gtk_menu_item_new_with_label("Close");
  gtk_menu_attach(menu_tomb, menu_close, 0, 1, 0, 1);
  g_signal_connect_swapped(menu_close, "activate", G_CALLBACK(cb_close), NULL);
  gtk_widget_show(menu_close);
  
  g_signal_connect_swapped(status_tomb, "activate", G_CALLBACK(left_click), menu_tomb);

  notice = notify_notification_new_with_status_icon
    ("Tomb encrypted undertaker",
     "We started digging out bones",
     NULL, status_tomb);
  notify_notification_set_icon_from_pixbuf(notice, pb_monmort);

  notify_notification_show(notice, &error);

  gtk_main();
  
  notify_uninit();

  exit(0);
  
}

// callbacks
gboolean left_click(GtkWidget *w, GdkEvent *e) {
  gtk_menu_popup(menu_tomb, NULL, NULL,
		 gtk_status_icon_position_menu, status_tomb,
		 1, gtk_get_current_event_time());
} 
gboolean cb_close(GtkWidget *w, GdkEvent *e) { 
  execlp("tomb","tomb","-S","umount",NULL);
  gtk_main_quit();
}
