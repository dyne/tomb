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

GdkPixbuf *pb_monmort;
GtkStatusIcon *status_tomb;
GtkMenu *menu_left, *menu_right;

NotifyNotification *notice;
GError *error;

char filename[256];
char mountpoint[256];

// forward declaration of callbacks
gboolean left_click(GtkWidget *w, GdkEvent *e);
gboolean cb_view(GtkWidget *w, GdkEvent *e);
gboolean cb_close(GtkWidget *w, GdkEvent *e);

gboolean right_click(GtkWidget *w, GdkEvent *e);
gboolean cb_about(GtkWidget *w, GdkEvent *e);


int main(int argc, char **argv) {
  GObject *tray;
  GtkWidget *item_close, *item_view, *item_about;
  gint menu_x, menu_y;
  gboolean push_in = true;

  char tomb_file[512];
  
  gtk_set_locale();
  gtk_init(&argc, &argv);

  // get the information from commandline
  if(argc<3) sprintf(mountpoint,"unknown");
  else snprintf(mountpoint,255, "%s", argv[2]);

  if(argc<2) sprintf(filename, "unknown");
  else snprintf(filename,255, "%s", argv[1]);

  // libnotify
  notify_init(PACKAGE);

  // set and show the status icon
  pb_monmort = gdk_pixbuf_new_from_xpm_data(monmort);
  status_tomb = gtk_status_icon_new_from_pixbuf(pb_monmort);
  //  gtk_status_icon_set_name(status_tomb, "tomb");
  gtk_status_icon_set_title(status_tomb, "Tomb");
  gtk_status_icon_set_tooltip_text (status_tomb, "Tomb - crypto undertaker");

  // LEFT click menu
  menu_left = (GtkMenu*) gtk_menu_new();
  // view
  item_view = gtk_menu_item_new_with_label("View");
  gtk_menu_attach(menu_left, item_view, 0, 1, 0, 1);
  g_signal_connect_swapped(item_view, "activate", G_CALLBACK(cb_view), NULL);
  gtk_widget_show(item_view);
  // close
  item_close = gtk_menu_item_new_with_label("Close");
  gtk_menu_attach(menu_left, item_close, 0, 1, 1, 2);
  g_signal_connect_swapped(item_close, "activate", G_CALLBACK(cb_close), NULL);
  gtk_widget_show(item_close);

  // connect it
  g_signal_connect_swapped(status_tomb, "activate", G_CALLBACK(left_click), menu_left);


  // RIGHT click menu
  menu_right = (GtkMenu*) gtk_menu_new();
  // about
  item_about = gtk_menu_item_new_with_label("About");
  gtk_menu_attach(menu_right, item_about, 0, 1, 0, 1);
  g_signal_connect_swapped(item_about, "activate", G_CALLBACK(cb_about), NULL);
  g_signal_connect_swapped(item_about, "popup-menu", G_CALLBACK(cb_about), NULL);
  gtk_widget_show(item_about);
  // connect it
  g_signal_connect_swapped(status_tomb, "popup-menu", G_CALLBACK(right_click), menu_right);

  // status icon
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

// callbacks left click
gboolean left_click(GtkWidget *w, GdkEvent *e) {
  gtk_menu_popup(menu_left, NULL, NULL,
		 gtk_status_icon_position_menu, status_tomb,
		 1, gtk_get_current_event_time());
} 
gboolean cb_view(GtkWidget *w, GdkEvent *e) { 
  GtkWidget *dialog = 
    gtk_message_dialog_new (NULL,
			    GTK_DIALOG_DESTROY_WITH_PARENT,
			    GTK_MESSAGE_INFO,
			    GTK_BUTTONS_CLOSE,
			    "Tomb '%s' open on '%s'", filename, mountpoint);
  gtk_dialog_run (GTK_DIALOG (dialog));
  gtk_widget_destroy (dialog);
  
}

gboolean cb_close(GtkWidget *w, GdkEvent *e) { 
  execlp("tomb","tomb","-S","umount",NULL);
  gtk_main_quit();
}

// callbacks right click
gboolean right_click(GtkWidget *w, GdkEvent *e) {
  gtk_menu_popup(menu_right, NULL, NULL,
		 gtk_status_icon_position_menu, status_tomb,
		 1, gtk_get_current_event_time());
} 
gboolean cb_about(GtkWidget *w, GdkEvent *e) {
  const gchar *authors[] = {"Denis Roio aka Jaromil - http://jaromil.dyne.org",NULL};
  const gchar *artists[] = {"Jordi aka MonMort - http://monmort.blogspot.org",
			    "Gabriele Zaverio aka Asbesto - http://freaknet.org/asbesto",
			    NULL};
  GtkWidget *dialog = gtk_about_dialog_new();
  gtk_about_dialog_set_name(GTK_ABOUT_DIALOG(dialog), PACKAGE);
  gtk_about_dialog_set_version(GTK_ABOUT_DIALOG(dialog), VERSION); 
  gtk_about_dialog_set_copyright(GTK_ABOUT_DIALOG(dialog), 
				 "(C)2007-2010 Denis Roio aka Jaromil");
  gtk_about_dialog_set_artists(GTK_ABOUT_DIALOG(dialog), artists);
  gtk_about_dialog_set_authors(GTK_ABOUT_DIALOG(dialog), authors);

  gtk_about_dialog_set_comments(GTK_ABOUT_DIALOG(dialog), 
				"The Crypto Undertaker\n"
"\n"
"This program helps people keeping their bones together by taking care of their private data inside encrypted storage filesystems that are easy to access and transport.\n"
"\n"
"The level of security provided by this program is fairly good: it uses an accelerated AES/SHA256 (cbc-essiv) to access the data on the fly, as if it would be a mounted volume.\n"
"\n"
"To start digging your tomb be ready to get your hands dirty and use the commandline utility 'tomb' from a text terminal."
);
  gtk_about_dialog_set_website(GTK_ABOUT_DIALOG(dialog), PACKAGE_URL);
  gtk_about_dialog_set_logo(GTK_ABOUT_DIALOG(dialog), pb_monmort);
  gtk_dialog_run(GTK_DIALOG (dialog));
  gtk_widget_destroy(dialog);
}
  
