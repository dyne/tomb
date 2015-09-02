#ifndef DIALOG_H
#define DIALOG_H

#include <QDialog>
#include <QWidget>
#include <QIcon>
#include <QSystemTrayIcon>
#include <QMenu>
#include <QAction>
#include <QDebug>
#include <QCoreApplication>
#include <QApplication>
#include <QDir>
#include <QDesktopServices>
#include <QUrl>
#include <QProcess>

class Tomb : public QDialog
{
    Q_OBJECT

    public:
        Tomb(QWidget *parent = 0);
        ~Tomb();


        QIcon icon;
        QSystemTrayIcon *trayIcon;
        QMenu *trayIconMenu;
        QAction *menu_tombExplore;
        QAction *menu_tombClose;
        QAction *menu_tombSlam;

    private:
        void tombBuildMenu();

        QString tombPath;
        QString tombName;
        QFileInfo info;
        QString tombMountPoint;

    private slots:
        virtual void closeEvent(QCloseEvent *event);

    public slots:
        void tombExplore();
        void tombClose();
        void tombSlam();
        void tombCheckCmdRet(int exitCode, QProcess::ExitStatus);
        void tombStartError(QProcess::ProcessError err);
};

#endif // DIALOG_H
