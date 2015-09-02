
#include "tomb.h"
#include <QDir>
#include <QStorageInfo>
#include <QMessageBox>
#include <QQuickView>

#include <mntent.h>

Tomb::Tomb(QWidget *parent)
    : QDialog(parent)
{
    struct mntent *ent;
    FILE *aFile;


    if (QApplication::arguments().length() > 1) {
        this->info = QFileInfo(QApplication::arguments().takeAt(1));
        this->tombName = QString(info.baseName());
        this->tombPath = info.path();
    } else {
        QMessageBox::critical(this, tr("tomb-qt-tray"), tr("You need to specify a Tomb File.\nExiting"), QMessageBox::Ok);
        exit(EXIT_FAILURE);
    }


    // Build the menù
    this->icon = QIcon( QCoreApplication::applicationDirPath() + QDir::separator()+QString("pixmaps/tomb_icon.png"));
    this->trayIcon = new QSystemTrayIcon(this->icon);
    this->trayIconMenu = new QMenu();

    this->tombBuildMenu();

    this->trayIcon->setContextMenu(this->trayIconMenu);

    this->trayIcon->setToolTip(QString(info.baseName()));
    this->trayIcon->show();
    this->trayIcon->showMessage(tr("Tomb encrypted undertaker"),tr("We started digging out bones"), QSystemTrayIcon::Information);
    if (QT_VERSION >= 0x050400) {
        for (auto volume : QStorageInfo::mountedVolumes()) {
            if (QString(volume.device()).contains(this->tombName) == true) {
                this->tombMountPoint = QString(volume.rootPath());
                break;
            }
        }
    } else {
         aFile = setmntent("/proc/mounts", "r");
         if (aFile == NULL) {
           perror("setmntent");
           exit(1);
         }
         while (NULL != (ent = getmntent(aFile))) {
             if (QString( ent->mnt_fsname).contains(this->tombName) == true) {
                 this->tombMountPoint = QString(ent->mnt_dir);
                 break;
             }
         }
         endmntent(aFile);
    }
}

void Tomb::closeEvent(QCloseEvent *event) {
    event->accept();
}

void Tomb::tombBuildMenu() {

    // Create the menu items
//    this->tombOpen = new QAction(tr("Open"), this);
    //this->trayIconMenu->addAction(tombOpen);

    this->menu_tombExplore = new QAction(tr("Explore"), this);
    this->trayIconMenu->addAction(menu_tombExplore);

    this->trayIconMenu->addSeparator();

    this->menu_tombClose = new QAction(tr("Close"), this);
    this->trayIconMenu->addAction(menu_tombClose);

    this->menu_tombSlam = new QAction(tr("Slam"), this);
    this->trayIconMenu->addAction(menu_tombSlam);

    connect(this->menu_tombExplore,  SIGNAL(triggered()), this, SLOT(tombExplore()));
    connect(this->menu_tombClose,  SIGNAL(triggered()), this, SLOT(tombClose()));
    connect(this->menu_tombSlam,  SIGNAL(triggered()), this, SLOT(tombSlam()));

}

void Tomb::tombExplore() {

    QDesktopServices::openUrl(QUrl(QUrl::fromLocalFile(this->tombMountPoint)));

}

void Tomb::tombClose() {

    QProcess *tomb;
    tomb = new QProcess(this);
    tomb->start("pkexec", QStringList() << "tomb" << "close");
    connect(tomb, SIGNAL(finished(int , QProcess::ExitStatus )), this, SLOT(tombCheckCmdRet(int , QProcess::ExitStatus )));
    connect(tomb, SIGNAL(error(QProcess::ProcessError)), this, SLOT(tombStartError(QProcess::ProcessError)));
    tomb->waitForFinished(30000);

}

void Tomb::tombSlam() {

    QProcess *tomb;
    tomb = new QProcess(this);
    tomb->start("pkexec", QStringList() << "tomb" << "slam");
    connect(tomb, SIGNAL(finished(int , QProcess::ExitStatus )), this, SLOT(tombCheckCmdRet(int , QProcess::ExitStatus )));
    connect(tomb, SIGNAL(error(QProcess::ProcessError)), this, SLOT(tombStartError(QProcess::ProcessError)));
    tomb->waitForFinished(30000);

}

void Tomb::tombCheckCmdRet(int exitCode, QProcess::ExitStatus exitStatus) {

    if (exitStatus == QProcess::CrashExit) {
        QMessageBox::critical(this, tr("tomb-qt-tray"), tr("polkit is not installed"),QMessageBox::Ok);
    } else {
        if (exitCode != QProcess::NormalExit) {
            QMessageBox::critical(this, tr("tomb-qt-tray"), tr("The program crashed\nTry to run 'tomb close' in a console"),QMessageBox::Ok);
        }
    }

}

void Tomb::tombStartError(QProcess::ProcessError err) {

    QString msg = QString();

    switch (err) {
        case QProcess::FailedToStart :
            msg = tr("The process failed to start. Either the invoked program is missing, or you may have insufficient permissions to invoke the program.");
        break;
        case QProcess::Crashed:
        case QProcess::Timedout:
        case QProcess::ReadError:
        case QProcess::WriteError:
        case QProcess::UnknownError:
            break;
    }
    QMessageBox::critical(this, tr("tomb-qt-tray"), msg, QMessageBox::Ok);

}


Tomb::~Tomb() {

}

