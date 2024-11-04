from FactorioSolver import FactorioSolver
from pathlib import Path
import pytest 
import pandas as pd

@pytest.fixture()
def data_folder():
   return Path(__file__).parent.joinpath("Data")
   
@pytest.fixture()
def test_preset(data_folder):
   return {
      "categories_filter" : list(pd.read_csv(data_folder.joinpath("test_categories.csv"))["name"]),
      "recipes_path":data_folder.joinpath("test_recipes.csv"),
      "items_path":data_folder.joinpath("test_items.csv"),
      "choice_map_path":data_folder.joinpath("test_choice_map.json")
   }

def test_contruction_default_res():
   model = FactorioSolver.Model()
   assert len(model.get_data_graph().vs) > 0
   assert len(model.get_data_graph().es) > 0
   assert len(model.get_products()) > 0
   assert len(model.get_recipes()) > 0

def test_contruction():
   model = FactorioSolver.Model()
   assert len(model.get_data_graph().vs) > 0
   assert len(model.get_data_graph().es) > 0
   assert len(model.get_products()) > 0
   assert len(model.get_recipes()) > 0

def test_get_choice_map():
   model = FactorioSolver.Model()
   choice_map = model.get_choice_map()
   assert not False in choice_map.apply(lambda x : x["Choice"] in x["Possibilities"], axis=1)
   
def test_get_product_usage_graph():
   model = FactorioSolver.Model()
   graph = model.get_product_usage_graph("inserter")
   assert(len(graph.vs) > 0)
   assert(len(graph.es) > 0)

def test_get_products_info():
   model = FactorioSolver.Model()
   info = model.get_products_info("belt")
   assert len(info["stack_size"]) > 0
   assert len(info) > 0

def test_get_choice_list(test_preset):
   model = FactorioSolver.Model(**test_preset)
   choice_list = model.get_choice_list()
   assert type(choice_list) == list
   assert len(choice_list) == 1

   choice_list = model.get_choice_list("item-a")
   assert len(choice_list) == 0

   choice_list = model.get_choice_list("item-abc")
   assert len(choice_list) == 1
   
   choice_list = model.get_choice_list("item-abc", model.get_choice_map())
   assert len(choice_list) == 0

def test_print_product_usage():
   model = FactorioSolver.Model()
   model.print_product_usage("inserter", show_fig=False)

def test_get_default_delivery_delta_time():
   model = FactorioSolver.Model()
   assert model.get_default_delivery_delta_time() > 0

def test_set_default_delivery_delta_time():
   model = FactorioSolver.Model()
   old = model.get_default_delivery_delta_time()
   model.set_default_delivery_delta_time(old + 1)
   assert model.get_default_delivery_delta_time() == old + 1

def test_compute_prod_graph(test_preset):
   model = FactorioSolver.Model(**test_preset)
   graph = model.compute_prod_graph({ "item-abc" : 2, "item-e" : 2 })
   assert len(graph.vs) > 0
   assert len(graph.es) > 0
   assert graph.vs["del_dt"].count(model.get_default_delivery_delta_time()) == len(graph.vs)

   new_freq = 20.0
   graph = model.compute_prod_graph({"item-abc":2 }, {"item-a":new_freq, "item-b":new_freq})
   assert graph.vs["del_dt"].count(model.get_default_delivery_delta_time()) == len(graph.vs) - 2
   assert graph.vs.select(name_eq="item-a")["del_dt"][0] == new_freq
   assert graph.vs.select(name_eq="item-b")["del_dt"][0] == new_freq

def test_print_production_single():
   model = FactorioSolver.Model()
   model.print_production_single("transport-belt", 2, {"stone":120, "copper-cable":120}, show_fig=False)

def test_print_production():
   model = FactorioSolver.Model()
   model.print_production({ "transport-belt" : 2, "logistic-science-pack":2 }, {"transport-belt":30.0}, show_fig=False)

def test_set_choice_map(test_preset):
   model = FactorioSolver.Model(**test_preset)
   graph = model.compute_prod_graph({"item-abc": 1})

   # default recipe crafts "item-abc" with "item-ab"
   assert len(graph.vs.select(name_eq="item-ab")) == 1
   datamap = model.get_choice_map()
   choice = datamap[datamap["Choice"] == "item-abc-pack"]
   assert len(choice) == 1
   assert "item-abc-pack" in choice.iloc[0]["Possibilities"]
   
   # make sure no ref is kept, the graph res should not have changed
   graph = model.compute_prod_graph({"item-abc": 1})
   assert len(graph.vs.select(name_eq="item-ab")) == 1

   # change it to "item-abs", which uses a, b and c directly
   datamap.loc[choice.index, "Choice"] = "item-abc"
   model.set_choice_map(datamap)
   graph = model.compute_prod_graph({"item-abc": 1})
   assert len(graph.vs.select(name_eq="item-ab")) == 0
   assert len(graph.vs.select(name_eq="item-a")) == 1
   assert len(graph.vs.select(name_eq="item-b")) == 1
   assert len(graph.vs.select(name_eq="item-c")) == 1

def test_global_shortcuts():
   FactorioSolver.get_products_info("belt")
   FactorioSolver.print_product_usage("inserter", show_fig=False)
   FactorioSolver.print_production_single("transport-belt", 2, {"stone":120, "copper-cable":120}, show_fig=False)
   FactorioSolver.print_production_single("automation-science-pack", 1, show_fig=False)   

def test_custom_preset(test_preset):
   model = FactorioSolver.Model(**test_preset)
   model.print_production_single("item-abc", 1, show_fig=False)

def test_space_exp_preset():
   model = FactorioSolver.Model(**FactorioSolver.Model.sSpaceExplorationPreset)
   model.print_production_single("se-rocket-science-pack", 1, show_fig=False)

def test_space_age_preset():
   model = FactorioSolver.Model(**FactorioSolver.Model.sSpaceAgePreset)
   model.print_production_single("rail-ramp", 1, show_fig=False)

if __name__ == "__main__":
   print(__name__, type(__name__)) 