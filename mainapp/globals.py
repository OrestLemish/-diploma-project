from django.utils.translation import gettext_lazy as _

SYSTEMS_VARIANTS = (('Debian(Linux)', _('Debian(Linux)')),
                    ('Red_Hat', _('Red Hat')),
                    ('other', _('other')),
                    )

SERVER_COMMANDS = {
    "Red_Hat": (
        ('yum install mc -y', _('install_mc')),
        ('yum install ncdu -y', _('install_ncdu')),

        ('useradd #new_username#;'
         'echo "#new_username#:#new_password#" | passwd --stdin #new_username#'
         'usermod -aG wheel #new_username#'
         'su - #new_username# -c "mkdir ~/.ssh";'
         'su - #new_username# -c "printf \'#id_rsa_pub#\' > /home/#new_username#/.ssh/authorized_keys";'
         'su - #new_username# -c "chmod 700 ~/.ssh";'
         'su - #new_username# -c "chmod 600 ~/.authorized_keys";'
         '?fghgfhghjghjhgjgfhj?',
         _('add new user (from root)')),

        ('mysql -u #username# -p #password# -e "create database #db_name#;',
         _('Create DB in MySQL')),

        ('mysqldump -u #username# -p #password# #database# > #backup_path#',
         _('Create Dump in MySQL')),

    ),
    "Debian(Linux)": (
        ('apt install mc -y', _('install_mc')),
        ('apt install ncdu -y', _('install_ncdu')),

        ('sudo adduser --disabled-password --gecos "" #new_username# && echo "#new_username#:#new_user_password#" | sudo chpasswd;'
         'sudo usermod -aG root #new_username# && sudo usermod -aG sudo #new_username#;'
         'su - #new_username# -c "mkdir ~/.ssh";'
         'su - #new_username# -c "printf \'#id_rsa_pub#\' > /home/#new_username#/.ssh/authorized_keys";'
         'su - #new_username# -c "chmod 700 ~/.ssh";'
         'su - #new_username# -c "chmod 600 ~/.authorized_keys";  ',
         _('add new user (from root)')),

        ('mysql -u #username# -p #password# -e "create database #db_name#;',
         _('Create DB in MySQL')),

        ('mysqldump -u #username# -p #password# #database# > #backup_path#',
         _('Create Dump in MySQL')),

        ('sudo apt update -y'
            'sudo apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev'
            'sudo apt-get install -y libssl-dev openssl python3-dev'
            'wget https://www.python.org/ftp/python/#version#/Python-#version#.tgz'
            'tar -xf Python-#version#.tgz'
            'cd Python-#version#/'
            './configure --enable-optimizations'
            'make -j $(nproc)'
            'sudo make altinstall',
         _('Install Python3')),

        ('sudo apt update -y'
            'sudo apt upgrade -y'
            'sudo apt install -y mysql-server libmysqlclient-dev'
            'sudo systemctl start mysql.service'
            'sudo mysql -e "ALTER USER \'root\'@\'localhost\' IDENTIFIED WITH mysql_native_password BY \'#password#\';"'
            'sudo mysql -e "exit"'
            'echo -e "n\ny\ny\ny\ny\n" | sudo mysql_secure_installation',
         _('Install MySQL')),

        ('sudo apt update -y'
            'sudo apt upgrade -y',
         _('Update server')),

        ('sudo timedatectl set-timezone #Timezone#',
         _('Change timezone')),

    ),
}
