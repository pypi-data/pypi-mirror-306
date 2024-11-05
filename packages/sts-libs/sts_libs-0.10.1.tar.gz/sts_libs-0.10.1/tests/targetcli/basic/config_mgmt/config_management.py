"""Test suite of targetcli saveconfig, clearconfig and restoreconfig."""

from __future__ import annotations

import gzip
from os import getenv
from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest

from sts.linux import count_files
from sts.lio import TargetCLI
from sts.utils.cmdline import run

# Parameters
target: TargetCLI = TargetCLI()
backups: int = int(getenv('BACKUP_NUMBER', '5'))
max_backup_files: int = int(getenv('MAX_BACKUP_FILES', '2'))

BACKUP_DIR = '/etc/target/backup/'


@pytest.mark.usefixtures('_target_test')
class TestSaveconfig:
    def test_saveconfig_cleanup(self) -> None:
        """Removes backups and saveconfig.json."""
        assert run('rm -f /etc/target/backup/*').succeeded
        assert run('rm -f /etc/target/saveconfig*.json').succeeded

    def test_saveconfig_backup(self) -> None:
        """There's only 1 backup file generated if no target change, no matter how many times running `targetcli
        saveconfig`.
        """
        # require backups >= 2, because backup file is generated at the second time of running saveconfig after a target
        # change
        assert backups >= 2
        for _ in range(backups):
            assert target.saveconfig() == 0

        number = count_files(BACKUP_DIR)
        assert number == 1, f'FAIL: In {BACKUP_DIR} there is more than 1 backup file.'

    def test_saveconfig_compare(self) -> None:
        """Compares last saved configuration with backup file."""
        # create an iscsi target
        target.path = '/iscsi/'
        for _ in range(3):
            assert target.create() == 0
        target.path = ''
        # save the configuration
        for _ in range(2):
            assert target.saveconfig() == 0
        # compare the content of the last saved /etc/target/saveconfig.json and /etc/target/backup/backup_file
        saveconfig = Path('/etc/target/saveconfig.json').read_text()

        backup_files = Path('/etc/target/backup/').glob('saveconfig-*')
        backup_file = max(backup_files, key=lambda item: item.stat().st_ctime)
        with gzip.open(backup_file, 'rt') as file:
            backup = file.read()

        assert saveconfig == backup, 'FAIL: Backup file is different than last saved configuration'

    def test_max_backup_files(self) -> None:
        """Creates maximum amount of backup files."""
        assert target.set(f'global max_backup_files={max_backup_files}') == 0
        assert target.get('global max_backup_files', return_output=True)[1] == f'max_backup_files={max_backup_files}'

        for _ in range(max_backup_files + 3):
            target.path = '/iscsi/'
            assert target.create() == 0
            target.path = ''
            assert target.saveconfig() == 0
            assert target.saveconfig() == 0

        number = count_files(BACKUP_DIR)
        assert number <= max_backup_files

    def test_saveconfig_savefile(self) -> None:
        """Saves configuration to a specified file."""
        with NamedTemporaryFile(prefix='saveconfig-') as temp_savefile:
            savefile: str = temp_savefile.name
            assert target.saveconfig(savefile=savefile) == 0
            assert Path(savefile).exists()

    def test_restoreconfig(self) -> None:
        """Restores configuration."""
        # Backup the current saveconfig
        current_config = Path('/etc/target/saveconfig.json')
        pre_config = current_config.with_stem('saveconfig_backup')
        pre_config.write_bytes(current_config.read_bytes())

        for _ in range(2):
            assert target.clearconfig() == 0
            assert target.restoreconfig(clearexisting=True) == 0
            assert target.saveconfig() == 0

        current = current_config.read_text()
        pre = pre_config.read_text()

        assert current == pre, 'FAIL: Current configuration is different than the base configuration'
