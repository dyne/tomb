/*  Tomb - encrypted storage undertaker
 *
 *  (c) Copyright 2015 Gianluca Montecchi <gian@grys.it>
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

#include <QApplication>
#include <QTranslator>
#include <QLocale>

#include "tomb.h"


int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    QTranslator translator(0);


    translator.load( QString("./i18n/tomb-qt-tray_") + QLocale::system().name() );

    a.installTranslator( &translator );
    //w.show();
    Tomb w;


    return a.exec();
}
