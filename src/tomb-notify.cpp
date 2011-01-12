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

// this file is a notification tool to send messages on the screen

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include <libnotify/notify.h>

/* The Tomb icon is an artwork by Jordi aka MonMort
   a nomadic graffiti artist from Barcelona */
#include <monmort.xpm>

int main(int argc, char **argv) {
  NotifyNotification *notice;
  GError *error;
  GdkPixbuf *pb_monmort;

  char title[256];
  char body[512];

  gtk_set_locale();
  gtk_init(&argc, &argv);

  // libnotify
  notify_init(PACKAGE);

  if(argc<3)
    snprintf(body,511, "I'm the crypto undertaker.\nLet's start digging out bones.");
  else
    snprintf(body,511, "%s", argv[2]);

  if(argc<2)
    snprintf(title,255,"%s version %s",PACKAGE,VERSION);
  else
    snprintf(title,255, "%s", argv[1]);
    
  // set the icon
  pb_monmort = gdk_pixbuf_new_from_xpm_data(monmort);

  notice = notify_notification_new(title, body, NULL, NULL);
  notify_notification_set_icon_from_pixbuf(notice, pb_monmort);

  notify_notification_show(notice, &error);

  notify_uninit();

  exit(0);
  
}
