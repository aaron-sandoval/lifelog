"""
Profiles the performance of the Timesheet main script execution.
"""

import cProfile
import pstats

# import Test2

catSuffix = '-PROF2'
cmd = f'MAIN.main(catalogSuffix="{catSuffix}, runPublic=False")'
prof = cProfile.Profile()
prof.run(cmd)
# prof.sort_stats('cumtime')
# prof.dump_stats('output.prof')
with open(f'PROFILE_MAIN_cat{catSuffix}.txt', 'w') as stream:
    stats = pstats.Stats(prof, stream=stream)
    stats.sort_stats('cumtime')
    stats.print_stats()