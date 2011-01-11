#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <gtk/gtk.h>

/* The Tomb icon is an artwork by Jordi aka MonMort
   a nomadic graffiti artist from Barcelona */
const char *monmort[] = {
/* columns rows colors chars-per-pixel */
"32 32 5 1",
"  c #000000",
". c #010101",
"X c #020202",
"o c #C1C1C1",
"O c None",
/* pixels */
"OO                            OO",
"O oooooooooooooooooooooooooooo O",
" oooooooooooooooooooooooooooooo ",
" oooooooooooooooooooooooooooooo ",
" oooooooo  X     oooooo     ooo ",
" oooooooo        oooooo     ooo ",
" oooooooo        oooooo     ooo ",
" oooooooo        oooooo     oooX",
" oooooooo    X   oooooo     ooo ",
" oooooooo        oooooo     ooo ",
" oooooooo       Xoooooo     ooo ",
" oooooooo        oooooo   X ooo ",
" oooooooo X      oooooo     ooo ",
" oooooooooooooooooooooooooooooo ",
" oooooooooooooooooooooo oooooooX",
" ooooooooooooooooooooooo oooooo ",
" oooooooooooooooo      X  ooooo ",
"O ooooooooooooooooooooooooooooo ",
"OO          oooooooooooooooooo O",
"OOOOOOOOOOOO oooo ooo ooo ooo OO",
"OOOOOOOOOOOOO ooo ooo oooXooo OO",
"OOOOOOOOOOOOO oooXooo ooo ooo OO",
"OOOOOOOOOOOOO ooo ooo ooo ooo OO",
"OOOOOOOOOOOOO ooo ooo ooo ooo OO",
"OOOOOOOOOOOOO ooo ooo ooo ooo OO",
"OOOOOOOOOOOOO ooo ooo ooo ooo OO",
"OOOOOOOOOOOOO ooo ooo ooo oooXOO",
"OOOOOOOOOOOOO ooo ooo ooo ooo OO",
"OOOOOOOOOOOOOXooo ooo ooo ooo OO",
"OOOOOOOOOOOOO ooooooooooooooo OO",
"OOOOOOOOOOOOOO ooooooooooooo OOO",
"OOOOOOOOOOOOOOO             OOOO"
};


GtkStatusIcon *status_tomb;
GtkMenu *menu_tomb;

// forward declaration of callbacks
gboolean left_click(GtkWidget *w, GdkEvent *e);
gboolean cb_open(GtkWidget *w, GdkEvent *e);
gboolean cb_quit(GtkWidget *w, GdkEvent *e);



int main(int argc, char **argv) {

  GObject *tray;
  GdkPixbuf *pb_monmort;
  GtkWidget *menu_open, *menu_close, *menu_quit;
  gint menu_x, menu_y;
  gboolean push_in = true;

  gtk_set_locale();
  gtk_init(&argc, &argv);

  // set and show the status icon
  pb_monmort = gdk_pixbuf_new_from_xpm_data(monmort);
  status_tomb = gtk_status_icon_new_from_pixbuf(pb_monmort);
  //  gtk_status_icon_set_name(status_tomb, "tomb");
  gtk_status_icon_set_title(status_tomb, "Tomb");
  gtk_status_icon_set_tooltip_text (status_tomb, "Tomb - encrypted storage undertaker");

  //  gtk_status_icon_set_blinking(status_tomb, true);
  menu_tomb = (GtkMenu*) gtk_menu_new();

  menu_open = gtk_menu_item_new_with_label("Open");
  gtk_menu_attach(menu_tomb, menu_open, 0, 1, 0, 1);
  g_signal_connect_swapped(menu_open, "activate", G_CALLBACK(cb_open), NULL);
  gtk_widget_show(menu_open);
  
  menu_close = gtk_menu_item_new_with_label("Close");
  gtk_menu_attach(menu_tomb, menu_close, 0, 1, 1, 2);
  gtk_widget_show(menu_close);

  menu_quit = gtk_menu_item_new_with_label("Quit");
  gtk_menu_attach(menu_tomb, menu_quit, 0, 1, 2, 3);
  g_signal_connect_swapped(menu_quit, "activate", G_CALLBACK(cb_quit), NULL);
  gtk_widget_show(menu_quit);

  g_signal_connect_swapped(status_tomb, "activate", G_CALLBACK(left_click), menu_tomb);

  gtk_main();

  exit(0);
  
  
}

// callbacks
gboolean left_click(GtkWidget *w, GdkEvent *e) {
  gtk_menu_popup(menu_tomb, NULL, NULL,
		 gtk_status_icon_position_menu, status_tomb,
		 1, gtk_get_current_event_time());
} 
gboolean cb_open(GtkWidget *w, GdkEvent *e) { 
  execlp("tomb","tomb","mount","sarcofago","/mnt/etrom",NULL);
}
gboolean cb_quit(GtkWidget *w, GdkEvent *e) { gtk_main_quit(); }
