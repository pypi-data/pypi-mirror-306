from sts.linux import module_test_helper
from sts.utils.cmdline import run


def test_target_core_mod() -> None:
    """Repeatedly load and unload the module."""
    module_test_helper('target_core_mod', 20)
    assert run('modinfo target_core_mod').succeeded
