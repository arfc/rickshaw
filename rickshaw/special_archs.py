"""Special archetypes provided as necessary to the Rickshaw input file. 
Used for fuel cycle niches that have more than just one incommodity and outcommodity
"""
import random 

def generate_throwsink(commod, name):
    vals = {}
    vals["capacity"] = 1e299
    vals["in_commods"] = {"val": [commod]} 
    config = {"name": name, "config": {"agents_sink": vals}}
    return config

def generate_throwsource(commod, name):
    vals = {}
    vals["capacity"] = 1e200
    vals["commod"] = commod
    vals["recipe_name"] = 'natural_uranium' 
    config = {"name": name, "config": {"agents_source": vals}}
    return config

def enrich_tails(name, vals, commod):
    vals[name] = 'tailcommod'
    sink = generate_throwsink('tailcommod', 'enrichsink')
    return sink

def sep_streams(name, vals, commod):
    sep_rand = random.uniform(0.0, 1.0)
    sep = 1 - (0.0000001)**(1-sep_rand)*(0.1)**sep_rand
    nucs = ["U", "Pu"]
    streams = {"streams":{
                  "item":[{
                      "commod": commod,
                      "info": {
                         "buf_size": 1e298,
                         "efficiencies": {
                             "item": []
                         }
                      }
                  }]       
              }}
    choice = random.choice(nucs)
    if choice == "U" or choice =="Pu":
        temp = {"comp": choice, "eff": sep}
        streams["streams"]["item"][0]["info"]["efficiencies"]["item"].append(temp)
    vals[name] = streams["streams"]
    return 0

def sep_leftover(name, vals, commod):
    vals[name] = 'leftovercommod'
    sink = generate_throwsink('leftovercommod', 'sepsink')
    return sink    

def ff_fill(name, vals, commod):
    vals[name] = {"val": 'fillcommod'}
    source = generate_throwsource('fillcommod', 'ffsource')
    return source

def ff_fill_recipe(name, vals, commod):
    vals[name] = "natural_uranium"
    return 0

def skip(name, vals, commod):
    return 0
