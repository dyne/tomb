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
