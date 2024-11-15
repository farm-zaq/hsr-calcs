import copy
from base_team import base_team
from s1_aven import s1_aven_team
from s1_aven_ss import s1_aven_team_ss
from e1_robin import e1_robin_team
from e1_aven import e1_aven_team
from s1_feixiao import s1_feixiao_team
from e1_feixiao import e1_feixiao_team
from st_feixiao import topaz_cone_team
from e1_topaz import e1_topaz_team

#TODO": technique
#TODO: windfall
#TODO: Unnerved

def calculate_damage(
  scaling_mult, extra_mult, scaling_attr, extra_dmg,
  crit_dmg,
  elemental_dmg_mult, all_type_dmg_mult,
  def_shred,
  res, res_pen,
  elemental_vuln, all_vuln,
  reductions,
  special_mult
  ):
  base_dmg = (scaling_mult + extra_mult) / 100 * scaling_attr + extra_dmg
  crit_mult = 1 + crit_dmg / 100
  dmg_mult = 1 + elemental_dmg_mult / 100 + all_type_dmg_mult / 100
  def_mult = (80.0 + 20.0) / ((82.0 + 20.0) * (1.0 - def_shred/100) + 80.0 + 20.0)
  res_mult = 1 - res / 100 + res_pen / 100
  vuln_mult = 1 + elemental_vuln / 100 + all_vuln / 100
  reduction_mult = 1
  for reduction in reductions:
    reduction_mult = reduction_mult * (1 - reduction / 100)
  special_mult = 1 + special_mult / 100
  dmg = base_dmg * crit_mult * dmg_mult * def_mult * res_mult * vuln_mult * reduction_mult * special_mult
  return dmg

def calculate_average_dmg(
  scaling_mult, extra_mult, scaling_attr, extra_dmg,
  crit_dmg, crit_rate,
  elemental_dmg_mult, all_type_dmg_mult,
  def_shred,
  res, res_pen,
  elemental_vuln, all_vuln,
  reductions,
  special_mult
  ):
  crit_damage = min(crit_rate / 100, 1) * calculate_damage(scaling_mult, extra_mult, scaling_attr, extra_dmg, crit_dmg, elemental_dmg_mult, all_type_dmg_mult, def_shred, res, res_pen, elemental_vuln, all_vuln, reductions, special_mult)
  no_crit_damage = max((1 - crit_rate / 100 ), 0) * calculate_damage(scaling_mult, extra_mult, scaling_attr, extra_dmg, 0, elemental_dmg_mult, all_type_dmg_mult, def_shred, res, res_pen, elemental_vuln, all_vuln, reductions, special_mult)
  dmg = crit_damage + no_crit_damage
  return dmg

def calculate_character_damage(unbuffed_char, in_buffs, attack_type, has_concerto):
  buffs = copy.deepcopy(in_buffs)
  applicable_buffs = buffs["base"]
  
  if attack_type in buffs:
    applicable_buffs += buffs[attack_type]
  if has_concerto:
    if f"concerto_{attack_type}" in buffs:
      applicable_buffs += buffs[f"concerto_{attack_type}"]
    if "concerto" in buffs:
      applicable_buffs += buffs["concerto"]

  char = buff(unbuffed_char, applicable_buffs)

  scaling_mult = char[f"{attack_type}_scaling"]

  extra_mult = char["extra_mult"]
  scaling_attr = char[char["scaling_attr"]]
  extra_dmg = char[f"{attack_type}_extra"]

  crit_dmg = char["crit_dmg"]
  crit_rate = char["crit_rate"]

  elemental_dmg_mult = char["elemental_dmg_mult"]
  all_type_dmg_mult = char["all_type_dmg_mult"]
  
  def_shred = char["def_shred"]
  
  res = char["res"]
  res_pen = char["res_pen"]
  
  elemental_vuln = char["elemental_vuln"]
  all_vuln = char["all_vuln"]
  
  reductions = char["reductions"]

  if "special_mult" in char:
    special_mult = char["special_mult"]
  else:
    special_mult = 0

  return calculate_average_dmg(
    scaling_mult, extra_mult, scaling_attr, extra_dmg,
    crit_dmg, crit_rate,
    elemental_dmg_mult, all_type_dmg_mult,
    def_shred,
    res, res_pen,
    elemental_vuln, all_vuln,
    reductions,
    special_mult
  )

def buff(char, buffs):
  buffed_char = copy.deepcopy(char)
  for buff in buffs:
    for key in buff:
      if key == "atk_percent":
        buffed_char["atk"] += buffed_char["base_atk"] * buff[key] / 100
      elif key == "defe_percent":
        buffed_char["defe"] += buffed_char["base_defe"] * buff[key] / 100
      else:
        buffed_char[key] += buff[key]
  return buffed_char

def team_damage(team_obj):
  robin = team_obj["robin"]
  robin_buffs = team_obj["robin_buffs"]
  feixiao = team_obj["feixiao"]
  feixiao_buffs = team_obj["feixiao_buffs"]
  topaz = team_obj["topaz"]
  topaz_buffs = team_obj["topaz_buffs"]
  aven = team_obj["aven"]
  aven_first_buffs = team_obj["aven_first_buffs"]
  aven_buffs = team_obj["aven_buffs"]

  robin_ult_dmg = calculate_character_damage(robin, robin_buffs, "ult", True)

  feixiao_skill_dmg = calculate_character_damage(feixiao, feixiao_buffs, "skill", False)
  feixiao_concerto_skill_dmg = calculate_character_damage(feixiao, feixiao_buffs, "skill", True)
  feixiao_fua_dmg = calculate_character_damage(feixiao, feixiao_buffs, "fua", False)
  feixiao_concerto_fua_dmg = calculate_character_damage(feixiao, feixiao_buffs, "fua", True)
  feixiao_concerto_ult_dmg = calculate_character_damage(feixiao, feixiao_buffs, "ult", True)

  topaz_basic_dmg = calculate_character_damage(topaz, topaz_buffs, "basic", False)
  topaz_concerto_basic_dmg = calculate_character_damage(topaz, topaz_buffs, "basic", True)
  topaz_skill_fua_dmg = calculate_character_damage(topaz, topaz_buffs, "fua", False)
  topaz_concerto_skill_fua_dmg = calculate_character_damage(topaz, topaz_buffs, "fua", True)

  aven_basic_dmg_first = calculate_character_damage(aven, aven_first_buffs, "basic", False)
  aven_basic_dmg_second = calculate_character_damage(aven, aven_buffs, "basic", False)
  aven_ult_dmg_first = calculate_character_damage(aven, aven_first_buffs, "ult", False)
  aven_ult_dmg_second = calculate_character_damage(aven, aven_buffs, "ult", False)
  aven_fua_first = calculate_character_damage(aven, aven_first_buffs, "fua", False)
  aven_concerto_fua_first = calculate_character_damage(aven, aven_first_buffs, "fua", True)
  aven_fua_second = calculate_character_damage(aven, aven_buffs, "fua", False)
  aven_concerto_fua_second = calculate_character_damage(aven, aven_buffs, "fua", True)

  feixiao_dmg = \
    feixiao_skill_dmg * 2 + \
    feixiao_concerto_skill_dmg * 4 + \
    feixiao_fua_dmg * 4 + \
    feixiao_concerto_fua_dmg * 8 + \
    feixiao_concerto_ult_dmg * 4

  topaz_dmg = \
    topaz_basic_dmg + \
    topaz_concerto_basic_dmg * 2 + \
    topaz_skill_fua_dmg * 5 + \
    topaz_concerto_skill_fua_dmg * 12 \

  aven_dmg = \
    aven_basic_dmg_first * 3 + \
    aven_basic_dmg_second * 3 + \
    aven_ult_dmg_first +  \
    aven_ult_dmg_second + \
    aven_fua_first * 2 + \
    aven_concerto_fua_first * 2 + \
    aven_fua_second * 2 + \
    aven_concerto_fua_second * 2 \
    
  robin_dmg = robin_ult_dmg * 44

  total_dmg = feixiao_dmg + topaz_dmg + aven_dmg + robin_dmg

  print(f"{team_obj['name']}:\t{total_dmg}")
  print(f"Feixiao:\t{feixiao_dmg}\t{feixiao_dmg / total_dmg * 100}")
  print(f"Topaz:\t\t{topaz_dmg}\t{topaz_dmg / total_dmg * 100}")
  print(f"Robin:\t\t{robin_dmg}\t{robin_dmg / total_dmg * 100}")
  print(f"Aven:\t\t{aven_dmg}\t{aven_dmg / total_dmg * 100}")
  print()

  return {
    "total_dmg": total_dmg,
    "feixiao_dmg": feixiao_dmg,
    "topaz_dmg": topaz_dmg,
    "aven_dmg": aven_dmg,
    "robin_dmg": robin_dmg,
    "cost": team_obj["cost"],
    "name": team_obj["name"],
  }

def team_damages(teams):
  damages = []
  for team in teams:
    damages.append(team_damage(team))
  return damages

# teams = [s1_aven_team, s1_aven_team_ss]
teams = [base_team, e1_robin_team, s1_aven_team, e1_aven_team, s1_feixiao_team, e1_feixiao_team, topaz_cone_team, e1_topaz_team]
damages = team_damages(teams)

def print_damage(damages):
  clean_damages = []
  for damage in damages:
    cost = damage["cost"]
    name = damage["name"]
    damage = damage["total_dmg"]
    percent_increase = int(100*damage/damages[0]['total_dmg'])
    if cost:
      increase_per_cost = (100*damage/damages[0]['total_dmg'] - 100) / cost
    else:
      increase_per_cost = 0
    clean_damages.append([name, damage, percent_increase, increase_per_cost])
  
  clean_damages = sorted(clean_damages, key=lambda x: x[3])
  for damage in clean_damages:
    name = damage[0]
    damage_num = damage[1]
    percent_increase = damage[2]
    increase_per_cost = damage[3]

    print(f"{name}\t{int(damage_num)}\t\t{percent_increase}\t\t{increase_per_cost}")

print_damage(damages)

# print(f"Total:\t{total_dmg}")
# print(f"Feixiao:\t{feixiao_dmg}\t{feixiao_dmg / total_dmg * 100}")
# print(f"Topaz:\t\t{topaz_dmg}\t{topaz_dmg / total_dmg * 100}")
# print(f"Robin:\t\t{robin_dmg}\t{robin_dmg / total_dmg * 100}")
# print(f"Aven:\t\t{aven_dmg}\t{aven_dmg / total_dmg * 100}")



