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
