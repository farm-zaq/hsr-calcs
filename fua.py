import copy
import json
import os

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

def pull_stats(base_data, upgrade_data, name):
  stats = base_data["stats"][name]
  if "stat_replacements" in upgrade_data:
    if name in upgrade_data["stat_replacements"]:
      for stat_name in upgrade_data["stat_replacements"][name]:
        stats[stat_name] = upgrade_data["stat_replacements"][name][stat_name]
  return stats

def pull_buffs(base_data, upgrade_data, name):
  buffs = copy.deepcopy(base_data["buff_applications"][name])

  for buff_group in buffs:
    buff_group_buffs = []
    for buff_name in buffs[buff_group]:
      removed_buff = False
      if "buff_removals" in upgrade_data:
        if name in upgrade_data["buff_removals"]:
          if buff_group in upgrade_data["buff_removals"][name]:
            if buff_name in upgrade_data["buff_removals"][name][buff_group]:
              removed_buff = True
      if not removed_buff:
        buff_group_buffs.append(base_data["buffs"][buff_name])
    buffs[buff_group] = buff_group_buffs

  if "buff_applications" in upgrade_data:
    if name in upgrade_data["buff_applications"]:
      for buff_group in upgrade_data["buff_applications"][name]:
        for buff_name in upgrade_data["buff_applications"][name][buff_group]:
          buffs[buff_group].append(upgrade_data["buffs"][buff_name])

  return buffs

def team_damage(base_data, upgrade_data):
  robin = pull_stats(base_data, upgrade_data, "robin")
  robin_buffs = pull_buffs(base_data, upgrade_data, "robin")
  feixiao = pull_stats(base_data, upgrade_data, "feixiao")
  feixiao_buffs = pull_buffs(base_data, upgrade_data, "feixiao")
  topaz = pull_stats(base_data, upgrade_data, "topaz")
  topaz_buffs = pull_buffs(base_data, upgrade_data, "topaz")
  aven = pull_stats(base_data, upgrade_data, "aven")
  aven_buffs = pull_buffs(base_data, upgrade_data, "aven")

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

  aven_basic_dmg = calculate_character_damage(aven, aven_buffs, "basic", False)
  aven_ult_dmg = calculate_character_damage(aven, aven_buffs, "ult", False)
  aven_fua = calculate_character_damage(aven, aven_buffs, "fua", False)
  aven_concerto_fua = calculate_character_damage(aven, aven_buffs, "fua", True)

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
    aven_basic_dmg * 6 + \
    aven_ult_dmg * 2 + \
    aven_fua * 4 + \
    aven_concerto_fua * 4
    
  robin_dmg = robin_ult_dmg * 44

  total_dmg = feixiao_dmg + topaz_dmg + aven_dmg + robin_dmg

  print(f"{upgrade_data['name']}\t{total_dmg}")
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
    "cost": upgrade_data["cost"],
    "name": upgrade_data["name"],
  }

teams_folder = "data/teams"

with open(f'{teams_folder}/base_team.json', 'r') as file:
  base_data = json.load(file)

with open('data/teams/no_upgrades.json', 'r') as file:
  upgrade_data = json.load(file)

def team_damages():
  damages = []
  with open(f'{teams_folder}/base_team.json', 'r') as file:
    base_data = json.load(file)
  for filename in os.listdir(teams_folder):
    if filename != "base_team.json":
      with open(f'data/teams/{filename}', 'r') as file:
        upgrade_data = json.load(file)
      damages.append(team_damage(copy.deepcopy(base_data), upgrade_data))
  return damages

damages = team_damages()

def print_damage(damages):
  damages = sorted(damages, key=lambda x: x["total_dmg"])
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


