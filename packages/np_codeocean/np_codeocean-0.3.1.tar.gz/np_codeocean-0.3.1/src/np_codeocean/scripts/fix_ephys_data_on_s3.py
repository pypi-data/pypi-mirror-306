import datetime
import logging
import pathlib
import npc_lims

import np_codeocean

logging.basicConfig(
    filename=f"logs/{pathlib.Path(__file__).stem}_{datetime.datetime.now().strftime('%Y-%d-%m_%H-%M-%S')}.log",
    level=logging.DEBUG, 
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s", 
    datefmt="%Y-%m-%d %H:%M:%S",
    )
logger = logging.getLogger(__name__)

session_id = 'ecephys_702136_2024-03-06_11-25-22'
root = npc_lims.get_raw_data_root(session_id)
ephys = root / 'ecephys_clipped'

np_codeocean.cleanup_ephys_symlinks(ephys)