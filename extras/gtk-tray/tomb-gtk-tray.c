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
#include <string.h>
#include <errno.h>
#include <libgen.h>

#include <sys/types.h>
#include <sys/wait.h>

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

char mapper[256];
char filename[256];
char mountpoint[256];

// forward declaration of callbacks
gboolean left_click(GtkWidget *w, GdkEvent *e);
gboolean cb_view(GtkWidget *w, GdkEvent *e);
gboolean cb_close(GtkWidget *w, GdkEvent *e);
gboolean cb_slam(GtkWidget *w, GdkEvent *e);

gboolean right_click(GtkWidget *w, GdkEvent *e);
gboolean cb_about(GtkWidget *w, GdkEvent *e);


int main(int argc, char **argv) {
  GtkWidget *item_close, *item_slam;
  GtkWidget *item_view, *item_about;
  gint menu_x, menu_y;
  gboolean push_in = TRUE;

  char tomb_file[512];
  char tooltip[256];

//  gtk_set_locale();
  gtk_init(&argc, &argv);

  // get the information from commandline
  if(argc<2) {
    fprintf(stderr, "error: need at least one argument, the name of an open tomb.\n");
    exit(1);
  } else {
    // TODO: check if mapper really exists
    snprintf(mapper,255, "%s", argv[1]);
  }

  snprintf(filename,255, "%s", argv[1]);
  snprintf(mountpoint,255, "/media/%s.tomb", argv[1]);

  // libnotify
  notify_init("Tomb");

  // set and show the status icon
  pb_monmort = gdk_pixbuf_new_from_xpm_data(monmort);
  status_tomb = gtk_status_icon_new_from_pixbuf(pb_monmort);
  //  gtk_status_icon_set_name(status_tomb, "tomb");
  gtk_status_icon_set_title(status_tomb, "Tomb");

  snprintf(tooltip,255,"%s",filename);
  gtk_status_icon_set_tooltip_text (status_tomb, tooltip);

  // LEFT click menu
  menu_left = (GtkMenu*) gtk_menu_new();
  // view
  item_view = gtk_menu_item_new_with_label("Explore");
  gtk_menu_attach(menu_left, item_view, 0, 1, 0, 1);
  g_signal_connect_swapped(item_view, "activate", G_CALLBACK(cb_view), NULL);
  gtk_widget_show(item_view);
  // close
  item_close = gtk_menu_item_new_with_label("Close");
  gtk_menu_attach(menu_left, item_close, 0, 1, 1, 2);
  g_signal_connect_swapped(item_close, "activate", G_CALLBACK(cb_close), NULL);
  gtk_widget_show(item_close);
  // slam
  item_slam = gtk_menu_item_new_with_label("Slam");
  gtk_menu_attach(menu_left, item_slam, 0, 1, 2, 3);
  g_signal_connect_swapped(item_slam, "activate", G_CALLBACK(cb_slam), NULL);
  gtk_widget_show(item_slam);

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
#if (HAVE_NOTIFY_NOTIFICATION_NEW_WITH_STATUS_ICON)
  notice = notify_notification_new_with_status_icon
    ("Tomb encrypted undertaker",
     "We started digging out bones",
     NULL, status_tomb);
#else
  notice = notify_notification_new
    ("Tomb encrypted undertaker",
     "We started digging out bones",
     NULL);
#endif
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
  return TRUE;
} 
gboolean cb_view(GtkWidget *w, GdkEvent *e) { 
  int pipefd[2];
  pid_t cpid;
  char buf;
  int c, res;
  char map[256];

  if (pipe(pipefd) <0) {
    fprintf(stderr,"pipe creation error: %s\n", strerror(errno));
    return FALSE;
  }

  cpid = fork();
  if (cpid == -1) {
    fprintf(stderr,"fork error: %s\n", strerror(errno));
    return FALSE;
  }
  if (cpid == 0) {    // Child
    close(pipefd[1]); // close unused write end
    for(c=0; read(pipefd[0], &buf, 1) > 0; c++)
      map[c] = buf;
    close(pipefd[0]);
    map[c] = 0;
    execlp("xdg-open", "xdg-open", map, (char*)NULL);
    _exit(1);
  }
  close(pipefd[0]); // close unused read end
  write(pipefd[1], mountpoint, strlen(mountpoint));
  close(pipefd[1]); // reader will see EOF

  return TRUE;
}


gboolean cb_close(GtkWidget *w, GdkEvent *e) { 
  int pipefd[2];
  pid_t cpid;
  char buf;
  int c, res;
  char map[256];

  if (pipe(pipefd) <0) {
    fprintf(stderr,"pipe creation error: %s\n", strerror(errno));
    return FALSE;
  }

  cpid = fork();
  if (cpid == -1) {
    fprintf(stderr,"fork error: %s\n", strerror(errno));
    return FALSE;
  }
  if (cpid == 0) {    // Child
    close(pipefd[1]); // close unused write end
    for(c=0; read(pipefd[0], &buf, 1) > 0; c++)
      map[c] = buf;
    close(pipefd[0]);
    map[c] = 0;
    execlp("tomb", "tomb", "close", map, (char*)NULL);
    _exit(1);
  }
  close(pipefd[0]); // close unused read end
  write(pipefd[1], mapper, strlen(mapper));
  close(pipefd[1]); // reader will see EOF

  waitpid(cpid, &res, 0);
  if(res==0) {
    gtk_main_quit();
    notify_uninit();
    exit(0);
  }
  /*  tomb-notify "Tomb '$tombname' is too busy."		\
      "Close all applications and file managers, then try again."
  */
  return TRUE;
}


gboolean cb_slam(GtkWidget *w, GdkEvent *e) {
  int pipefd[2];
  pid_t cpid;
  char buf;
  int c, res;
  char map[256];

  if (pipe(pipefd) <0) {
    fprintf(stderr,"pipe creation error: %s\n", strerror(errno));
    return FALSE;
  }

  cpid = fork();
  if (cpid == -1) {
    fprintf(stderr,"fork error: %s\n", strerror(errno));
    return FALSE;
  }
  if (cpid == 0) {    // Child
    close(pipefd[1]); // close unused write end
    for(c=0; read(pipefd[0], &buf, 1) > 0; c++)
      map[c] = buf;
    close(pipefd[0]);
    map[c] = 0;
    execlp("tomb", "tomb", "slam", map, (char*)NULL);
    _exit(1);
  }
  close(pipefd[0]); // close unused read end
  write(pipefd[1], mapper, strlen(mapper));
  close(pipefd[1]); // reader will see EOF

  waitpid(cpid, &res, 0);
  if(res==0) {
    gtk_main_quit();
    notify_uninit();
    exit(0);
  }
  /*  tomb-notify "Tomb '$tombname' is too busy."		\
      "Close all applications and file managers, then try again."
  */
  return TRUE;
}

// callbacks right click
gboolean right_click(GtkWidget *w, GdkEvent *e) {
  gtk_menu_popup(menu_right, NULL, NULL,
		 gtk_status_icon_position_menu, status_tomb,
		 1, gtk_get_current_event_time());
  return TRUE;
} 
gboolean cb_about(GtkWidget *w, GdkEvent *e) {
  const gchar *authors[] = {"Jaromil - http://jaromil.dyne.org",
			    "Code reviews and contributions by:",
			    "Dreamer, Hellekin O. Wolf, Shining, Mancausoft,",
			    "Anathema, Boyska and Nignux", NULL};
  const gchar *artists[] = {"Món Mort - http://monmort.blogspot.com",
			    "Asbesto Molesto - http://freaknet.org/asbesto",
			    NULL};
  GtkWidget *dialog = gtk_about_dialog_new();
//  gtk_about_dialog_set_name(GTK_ABOUT_DIALOG(dialog), "Tomb GTK Tray");
  gtk_about_dialog_set_version(GTK_ABOUT_DIALOG(dialog), "1.4"); 
  gtk_about_dialog_set_copyright(GTK_ABOUT_DIALOG(dialog), 
				 "(C)2007-2013 Jaromil @ Dyne.org Foundation");
  gtk_about_dialog_set_artists(GTK_ABOUT_DIALOG(dialog), artists);
  gtk_about_dialog_set_authors(GTK_ABOUT_DIALOG(dialog), authors);

  gtk_about_dialog_set_comments(GTK_ABOUT_DIALOG(dialog), 
				"The Crypto Undertaker\n"
"\n"
"This program helps people keeping their bones together by taking care of their private data inside encrypted storage filesystems that are easy to access and transport.\n"
"\n"
"The level of security provided by this program is fairly strong: it uses  AES/SHA256 (cbc-essiv) to access the encrypted volumes in realtime so that all what is physically stored on your disc is only in an encrypted form.\n"
"Tomb also encourages users to separate keys from data, for instance storing them on USB.\n"
"\n"
);
  gtk_about_dialog_set_website(GTK_ABOUT_DIALOG(dialog), "http://tomb.dyne.org");
  gtk_about_dialog_set_logo(GTK_ABOUT_DIALOG(dialog), pb_monmort);
  gtk_about_dialog_set_logo_icon_name(GTK_ABOUT_DIALOG(dialog), "monmort");
  // this below is active since gtk 3.0 so too early for it now
  //  gtk_about_dialog_set_license_type(GTK_ABOUT_DIALOG(dialog), GtkLicense.GTK_LICENSE_GPL_3_0);
  gtk_about_dialog_set_license(GTK_ABOUT_DIALOG(dialog),
"This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.\n"
"\n"
"This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.\n"
"\n"
"You should have received a copy of the GNU General Public License along with this program.\n"
"If not, see <http://www.gnu.org/licenses>\n"
"\n"
" The latest Tomb sourcecode is published on <http://tomb.dyne.org>\n");
  gtk_about_dialog_set_wrap_license(GTK_ABOUT_DIALOG(dialog), TRUE);
  gtk_dialog_run(GTK_DIALOG (dialog));
  gtk_widget_destroy(dialog);
  return TRUE;
}
  

  // GtkWidget *dialog = 
  //   gtk_message_dialog_new (NULL,
  // 			    GTK_DIALOG_DESTROY_WITH_PARENT,
  // 			    GTK_MESSAGE_INFO,
  // 			    GTK_BUTTONS_CLOSE,
  // 			    "Tomb '%s' open on '%s'\n"
  // 			    "device mapper: %s", filename, mountpoint, mapper);
  // gtk_dialog_run (GTK_DIALOG (dialog));
  // gtk_widget_destroy (dialog);
