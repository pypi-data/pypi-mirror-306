from flightanalysis.builders.schedules.f3a_p23 import p23_def
from flightanalysis.builders.schedules.f3a_a25 import a25_def
from flightanalysis.builders.schedules.f3a_p25 import p25_def
from flightanalysis.builders.schedules.f3a_f25 import f25_def
#from imac_unlim2024 import sdef as imac_unl2024_def
from flightanalysis.builders.schedules.f3auk_clubman import clubman_def as f3auk_club_def
from flightanalysis.builders.schedules.f3auk_intermediate import intermediate_def as f3auk_int_def
from flightanalysis.builders.schedules.baeaglid_intermediate import sdef as baeaglid_intermediate_def
from flightanalysis.builders.schedules.baeapower_unlimited2024 import sdef as baeapower_unlimited2024_def
from flightanalysis.builders.schedules.baeapower_advanced2024 import sdef as baeapower_advanced2024_def
from flightanalysis.builders.schedules.iac_advanced2024 import sdef as iac_advanced2024_def
from flightanalysis import ScheduleInfo
sdefs = {
    'f3a_p23_schedule': p23_def, 
    'f3a_a25_schedule': a25_def, 
    'f3a_p25_schedule': p25_def, 
    'f3a_f25_schedule': f25_def, 
    #'IMAC_Unlimited2024_schedule': imac_unl2024_def, 
    'f3auk_clubman_schedule': f3auk_club_def, 
    'f3auk_inter_schedule': f3auk_int_def,
    "baeaglid_intermediate_schedule": baeaglid_intermediate_def,
    "baeapower_unlimited2024_schedule": baeapower_unlimited2024_def,
    "baeapower_advanced2024_schedule": baeapower_advanced2024_def,
    "iac_advanced2024_schedule": iac_advanced2024_def
}

def create_all():
    for k, sdef in sdefs.items():
        
        sdef.to_json(f"flightanalysis/data/{k}.json", ScheduleInfo.from_str(k))

if __name__ == '__main__':
    create_all()