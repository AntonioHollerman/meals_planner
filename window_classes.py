import os.path

from holding_functions import *
import tkinter as tk
from tkinter import ttk, filedialog
from random import choice
from PIL import Image, ImageTk
from typing import Dict


class RecipesWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        holding_recipes: List[recipe_row] = all_saved_recipes()
        self.recipes: Dict[int: recipe_row] = {}
        self.breakfasts: Dict[int: recipe_row] = {}
        self.lunches: Dict[int: recipe_row] = {}
        self.dinners: Dict[int: recipe_row] = {}
        for recipe in recipes_for_meal_type('breakfast'):
            self.breakfasts[recipe.recipe_id] = recipe
        for recipe in recipes_for_meal_type('lunch'):
            self.lunches[recipe.recipe_id] = recipe
        for recipe in recipes_for_meal_type('dinner'):
            self.dinners[recipe.recipe_id] = recipe

        if not self.breakfasts:
            new_id = add_recipe('None', [], 'None', 'Nothing Here', 'None',
                                "file_location", 'breakfast')
            self.breakfasts[new_id] = recipe_row(new_id, 'None', [], 'None', 'Nothing Here', 'None', "file_location",
                                                 'breakfast')
        if not self.lunches:
            new_id = add_recipe('None', [], 'None', 'Nothing Here', 'None',
                                "file_location", 'breakfast')
            self.lunches[new_id] = recipe_row(new_id, 'None', [], 'None', 'Nothing Here', 'None', "file_location",
                                              'lunch')
        if not self.dinners:
            new_id = add_recipe('None', [], 'None', 'Nothing Here', 'None',
                                "file_location", 'breakfast')
            self.dinners[new_id] = recipe_row(new_id, 'None', [], 'None', 'Nothing Here', 'None', "file_location",
                                              'dinner')

        self.breakfast_recipe = choice(list(self.breakfasts.values()))
        self.lunch_recipe = choice(list(self.lunches.values()))
        self.dinner_recipe = choice(list(self.dinners.values()))

        if holding_recipes:
            self.current_recipe = choice(holding_recipes)
        else:
            self.current_recipe = None

        self.current_window = MealsFrame(self)
        self.frame_displayed = 'Meals Frame'
        self.current_meal = "breakfasts"

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.current_window.grid(row=0, column=0, sticky="nesw")

    def swap_frame(self, framed_wanted):
        self.current_window.destroy()
        if isinstance(self.current_window, HomeFrame):
            if self.current_window.current_recipe_frame.new_image is not None:
                new_recipe = recipe_row(self.current_recipe.recipe_id, self.current_recipe.recipe_name,
                                        self.current_recipe.recipe_ingredients,
                                        self.current_window.current_recipe_frame.new_image,
                                        self.current_recipe.recipe_desc, self.current_recipe.recipe_instructions,
                                        self.current_recipe.instructions_type, self.current_recipe.meal_type)
                self.recipes[self.current_recipe.recipe_id] = new_recipe
                self.current_recipe = new_recipe
                self.current_window.new_image = None
        elif isinstance(self.current_window, EditFrame):
            if self.current_window.new_image is not None:
                new_recipe = recipe_row(self.current_recipe.recipe_id, self.current_recipe.recipe_name,
                                        self.current_recipe.recipe_ingredients, self.current_window.new_image,
                                        self.current_recipe.recipe_desc, self.current_recipe.recipe_instructions,
                                        self.current_recipe.instructions_type, self.current_recipe.meal_type)
                self.recipes[self.current_recipe.recipe_id] = new_recipe
                self.current_recipe = new_recipe
                self.current_window.new_image = None
        else:
            if self.current_meal == "breakfast":
                self.current_recipe = self.breakfast_recipe
            elif self.current_meal == 'lunch':
                self.current_recipe = self.lunch_recipe
            else:
                self.current_recipe = self.dinner_recipe
            if self.current_window.breakfast_frame.new_image is not None:
                new_recipe = recipe_row(self.breakfast_recipe.recipe_id, self.breakfast_recipe.recipe_name,
                                        self.breakfast_recipe.recipe_ingredients,
                                        self.current_window.breakfast_frame.new_image,
                                        self.breakfast_recipe.recipe_desc, self.breakfast_recipe.recipe_instructions,
                                        self.breakfast_recipe.instructions_type, self.breakfast_recipe.meal_type)
                self.breakfasts[self.breakfast_recipe.recipe_id] = new_recipe
                self.current_window.new_image = None
                self.current_recipe = new_recipe
            if self.current_window.lunch_frame.new_image is not None:
                new_recipe = recipe_row(self.lunch_recipe.recipe_id, self.lunch_recipe.recipe_name,
                                        self.lunch_recipe.recipe_ingredients,
                                        self.current_window.lunch_frame.new_image,
                                        self.lunch_recipe.recipe_desc, self.lunch_recipe.recipe_instructions,
                                        self.lunch_recipe.instructions_type, self.lunch_recipe.meal_type)
                self.lunches[self.lunch_recipe.recipe_id] = new_recipe
                self.current_window.new_image = None
                self.current_recipe = new_recipe
            if self.current_window.dinner_frame.new_image is not None:
                new_recipe = recipe_row(self.dinner_recipe.recipe_id, self.dinner_recipe.recipe_name,
                                        self.dinner_recipe.recipe_ingredients,
                                        self.current_window.dinner_frame.new_image,
                                        self.dinner_recipe.recipe_desc, self.dinner_recipe.recipe_instructions,
                                        self.dinner_recipe.instructions_type, self.dinner_recipe.meal_type)
                self.dinners[self.dinner_recipe.recipe_id] = new_recipe
                self.current_window.new_image = None
                self.current_recipe = new_recipe
        if framed_wanted == 'Edit Frame':
            self.frame_displayed = 'Edit Frame'
            self.current_window = EditFrame(self, self.current_recipe)
            self.current_window.grid(row=0, column=0, sticky="nesw")
        elif framed_wanted == 'Home Frame':
            self.frame_displayed = 'Home Frame'
            self.current_window = HomeFrame(self, self.current_recipe)
            self.current_window.grid(row=0, column=0, sticky="nesw")
        else:
            if self.current_meal == "breakfast":
                self.breakfasts = self.recipes.copy()
            elif self.current_meal == 'lunch':
                self.lunches = self.recipes.copy()
            else:
                self.dinners = self.recipes.copy()
            self.frame_displayed = 'Meals Frame'
            self.current_window = MealsFrame(self)
            self.current_window.grid(row=0, column=0, sticky="nesw")


class HomeFrame(ttk.Frame):
    def __init__(self, master: RecipesWindow, recipe: recipe_row):
        super().__init__(master)
        self.master_win = master
        self.current_recipe_frame = CurrentRecipeFrame(self, recipe)
        self.current_recipe = recipe

        self.random_button = ttk.Button(self, text="Random", command=self.random_recipe)
        self.next_button = ttk.Button(self, text="-->", command=self.next_recipe)
        self.back_button = ttk.Button(self, text="<--", command=self.previous_recipe)
        self.edit_button = ttk.Button(self, text="Edit", command=self.edit_button)
        self.crate_button = ttk.Button(self, text="Add New Recipe", command=self.create_recipe)
        self.delete_button = ttk.Button(self, text="Delete", command=self.delete_recipe)
        self.meals_button = ttk.Button(self, text="Back", command=self.meals_frame)

        ttk.Label(self, text="Your recipes are below", justify="center", anchor="center").grid(row=0,
                                                                                               column=1, sticky="ew")
        ttk.Separator(self).grid(row=1, column=0, columnspan=3, sticky="ew")
        self.random_button.grid(row=2, column=1)
        self.back_button.grid(row=3, column=0, sticky="w")
        self.next_button.grid(row=3, column=2, sticky="e")
        self.edit_button.grid(row=4, column=0, sticky="w")
        self.crate_button.grid(row=4, column=2, sticky="e")
        self.delete_button.grid(row=4, column=1, sticky="n")
        self.meals_button.grid(row=0, column=0, sticky="w")
        self.current_recipe_frame.grid(row=3, column=1, sticky="nesw")

        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=3)
        self.rowconfigure(3, weight=9)
        self.rowconfigure(4, weight=3)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)
        self.columnconfigure(2, weight=1)

        if any(recipe_id > recipe.recipe_id for recipe_id in self.master_win.recipes.keys()):
            self.next_button["state"] = "normal"
        else:
            self.next_button["state"] = "disabled"

        if any(recipe_id < recipe.recipe_id for recipe_id in self.master_win.recipes.keys()):
            self.back_button["state"] = "normal"
        else:
            self.back_button["state"] = "disabled"

        if not self.master_win.recipes:
            self.create_recipe()

    def next_recipe(self):
        available_ids = list(filter(next_id_filter(self.current_recipe.recipe_id), self.master_win.recipes.keys()))
        available_ids.sort()
        if available_ids:
            new_current_recipe = self.master_win.recipes[available_ids[0]]
            self.current_recipe = new_current_recipe
            self.master_win.current_recipe = new_current_recipe
            self.current_recipe_frame.refresh(new_current_recipe)
        if any(recipe_id > self.current_recipe.recipe_id for recipe_id in self.master_win.recipes.keys()):
            self.next_button["state"] = "normal"
        else:
            self.next_button["state"] = "disabled"

        if any(recipe_id < self.current_recipe.recipe_id for recipe_id in self.master_win.recipes.keys()):
            self.back_button["state"] = "normal"
        else:
            self.back_button["state"] = "disabled"

    def previous_recipe(self):
        available_ids = list(filter(previous_id_filter(self.current_recipe.recipe_id), self.master_win.recipes.keys()))
        available_ids.sort(reverse=True)
        if available_ids:
            new_current_recipe = self.master_win.recipes[available_ids[0]]
            self.current_recipe = new_current_recipe
            self.master_win.current_recipe = new_current_recipe
            self.current_recipe_frame.refresh(new_current_recipe)
        if any(recipe_id > self.current_recipe.recipe_id for recipe_id in self.master_win.recipes.keys()):
            self.next_button["state"] = "normal"
        else:
            self.next_button["state"] = "disabled"

        if any(recipe_id < self.current_recipe.recipe_id for recipe_id in self.master_win.recipes.keys()):
            self.back_button["state"] = "normal"
        else:
            self.back_button["state"] = "disabled"

    def random_recipe(self):
        available_ids = list(self.master_win.recipes.keys())
        available_ids.remove(self.current_recipe.recipe_id)
        if available_ids:
            new_current_recipe = self.master_win.recipes[choice(available_ids)]
            self.current_recipe = new_current_recipe
            self.master_win.current_recipe = new_current_recipe
            self.current_recipe_frame.refresh(new_current_recipe)
        if any(recipe_id > self.current_recipe.recipe_id for recipe_id in self.master_win.recipes.keys()):
            self.next_button["state"] = "normal"
        else:
            self.next_button["state"] = "disabled"

        if any(recipe_id < self.current_recipe.recipe_id for recipe_id in self.master_win.recipes.keys()):
            self.back_button["state"] = "normal"
        else:
            self.back_button["state"] = "disabled"

    def create_recipe(self):
        new_id = add_recipe('Recipe Name Here', ['Edit Ingredients'], 'None',
                            'Add Description', 'None', 'None',
                            self.master_win.current_meal)
        self.current_recipe = recipe_row(new_id, 'Recipe Name Here', ['Edit Ingredients'], 'None', 'Add Description',
                                         'None', 'None', self.master_win.current_meal)
        self.master_win.current_recipe = self.current_recipe
        self.master_win.recipes[new_id] = self.current_recipe
        self.current_recipe_frame.refresh(self.current_recipe)

        if any(recipe_id > self.current_recipe.recipe_id for recipe_id in self.master_win.recipes.keys()):
            self.next_button["state"] = "normal"
        else:
            self.next_button["state"] = "disabled"

        if any(recipe_id < self.current_recipe.recipe_id for recipe_id in self.master_win.recipes.keys()):
            self.back_button["state"] = "normal"
        else:
            self.back_button["state"] = "disabled"

    def delete_recipe(self):
        old_id = self.current_recipe.recipe_id
        if any(recipe_id > self.current_recipe.recipe_id for recipe_id in self.master_win.recipes.keys()):
            self.next_recipe()
        elif any(recipe_id < self.current_recipe.recipe_id for recipe_id in self.master_win.recipes.keys()):
            self.previous_recipe()
        else:
            self.create_recipe()
        del self.master_win.recipes[old_id]

        if any(recipe_id > self.current_recipe.recipe_id for recipe_id in self.master_win.recipes.keys()):
            self.next_button["state"] = "normal"
        else:
            self.next_button["state"] = "disabled"
        if any(recipe_id < self.current_recipe.recipe_id for recipe_id in self.master_win.recipes.keys()):
            self.back_button["state"] = "normal"
        else:
            self.back_button["state"] = "disabled"

    def edit_button(self):
        self.master_win.swap_frame('Edit Frame')

    def meals_frame(self):
        if self.master_win.current_meal == "breakfast":
            self.master_win.breakfast_recipe = self.current_recipe
            self.master_win.breakfasts = self.master_win.recipes
        elif self.master_win.current_meal == "lunch":
            self.master_win.lunch_recipe = self.current_recipe
            self.master_win.lunches = self.master_win.recipes
        else:
            self.master_win.dinner_recipe = self.current_recipe
            self.master_win.dinners = self.master_win.recipes
        self.master_win.swap_frame('Meals Frame')


class CurrentRecipeFrame(ttk.Frame):
    def __init__(self, master: HomeFrame, recipe: recipe_row):
        super().__init__(master)
        self.home_frame = master
        self.recipe_info = recipe_row
        self.tk_widgets: List[ttk.Separator | ttk.Button | ttk.Label] = []
        self.recipe_photo = None
        self.new_image = None

        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=8)
        self.rowconfigure(2, weight=3)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.refresh(recipe)

    def refresh(self, recipe: recipe_row):
        if self.tk_widgets:
            for widget in self.tk_widgets:
                widget.destroy()
            self.tk_widgets = []
        recp = self.recipe_info
        if self.new_image is not None:
            new_recipe = recipe_row(recp.recipe_id, recp.recipe_name, recp.recipe_ingredients, self.new_image,
                                    recp.recipe_desc, recp.recipe_instructions, recp.instructions_type,
                                    self.home_frame.master_win.current_meal)
            self.home_frame.master_win.recipes[recp.recipe_id] = new_recipe
            self.new_image = None

        self.recipe_info = recipe
        recipe_title = ttk.Label(self, text=recipe.recipe_name, anchor="center", justify="center")
        ingredients_label = ttk.Label(self, text="Ingredients", anchor="center", justify="center")
        line_seperator = ttk.Separator(self)
        ingredients_list_box = tk.Listbox(self, height=len(recipe.recipe_ingredients))
        open_instruction_button = ttk.Button(self, text="Open: ", command=self.open_instructions)
        instructions_location_label = ttk.Label(self, text=recipe.recipe_instructions, anchor="e", justify="left")
        for ingredient in recipe.recipe_ingredients:
            ingredients_list_box.insert(tk.END, ingredient)
        ingredients_list_box["state"] = "disabled"

        recipe_title.grid(row=0, column=0, sticky="ew")
        ingredients_label.grid(row=0, column=1, sticky="ew")
        ingredients_list_box.grid(row=1, column=1, sticky="nesw")
        open_instruction_button.grid(row=2, column=0, sticky="e")
        instructions_location_label.grid(row=2, column=1, sticky="ew")

        self.tk_widgets.append(recipe_title)
        self.tk_widgets.append(ingredients_label)
        self.tk_widgets.append(ingredients_list_box)
        self.tk_widgets.append(line_seperator)
        self.tk_widgets.append(open_instruction_button)
        self.tk_widgets.append(instructions_location_label)

        if recipe.recipe_image != "None" and os.path.exists(recipe.recipe_image):
            try:
                self.display_image(True, recipe.recipe_image)
            except Exception as err:
                self.display_image(False)
                print(err)
        else:
            self.display_image(False)

    def open_instructions(self):
        open_instructions(self.recipe_info.recipe_id)

    def display_image(self, file_found, recipe_path=None):
        if file_found:
            recipe_image = Image.open(recipe_path)
            self.recipe_photo = ImageTk.PhotoImage(recipe_image)
            recipe_label = ttk.Label(self, image=self.recipe_photo)
            recipe_label.grid(row=1, column=0)
            self.tk_widgets.append(recipe_label)
        else:
            image_button = ttk.Button(self, text="select image", command=self.select_image)
            image_button.grid(row=1, column=0)
            self.tk_widgets.append(image_button)

    def select_image(self):
        image_path = filedialog.askopenfilename()
        try:
            self.display_image(True, image_path)
            self.new_image = image_path
        except Exception as err:
            print(err)


class EditFrame(ttk.Frame):
    def __init__(self, master: RecipesWindow, recipe: recipe_row):
        super().__init__(master)
        self.master_win = master
        self.recipe_info = recipe
        self.ingredients_frame = IngredientsListFrame(self)
        self.tk_website_link = tk.StringVar(self)
        self.tk_fileloc = tk.StringVar(self)
        self.new_image = None
        self.recipe_photo = None

        if recipe.instructions_type == "web_link":
            self.tk_website_link.set(recipe.recipe_instructions)
        if recipe.instructions_type == "file_location":
            self.tk_fileloc.set(recipe.recipe_instructions)

        self.tk_recipe_instruc_type = tk.StringVar(self, value=recipe.instructions_type)
        self.weblink_radio = ttk.Radiobutton(self, value="web_link", variable=self.tk_recipe_instruc_type,
                                             text="Web site: ")
        self.fileloc_radio = ttk.Radiobutton(self, value="file_location", variable=self.tk_recipe_instruc_type,
                                             text="File Location: ")
        self.weblink_entry = ttk.Entry(self, textvariable=self.tk_website_link)
        self.fileloc_entry = ttk.Entry(self, textvariable=self.tk_fileloc)
        self.fileloc_button = ttk.Button(self, text="Select File", command=self.select_file)
        self.back_button = ttk.Button(self, text="<- Back", command=self.back_button_command)
        self.reset_button = ttk.Button(self, text="Reset", command=self.reset_button_command)
        self.change_image_button = ttk.Button(self, text="Change Image", command=self.select_image)

        self.tk_recipe_title = tk.StringVar(self, value=recipe.recipe_name)
        self.title_entry = ttk.Entry(self, textvariable=self.tk_recipe_title)
        self.desc_box = tk.Text(self, height=5)
        self.desc_box.insert("1.0", recipe.recipe_desc)

        self.weblink_radio.grid(row=1, column=0, sticky="e", padx=3, pady=3)
        self.fileloc_radio.grid(row=2, column=0, sticky="e", padx=3, pady=3)
        self.weblink_entry.grid(row=1, column=1, sticky="we", padx=3, pady=3)
        self.fileloc_entry.grid(row=2, column=1, sticky="we", padx=3, pady=3)
        self.fileloc_button.grid(row=3, column=1, sticky="n", padx=3, pady=3)
        self.change_image_button.grid(row=3, column=0)
        self.back_button.grid(row=4, column=0, sticky="w", padx=3, pady=3)
        self.reset_button.grid(row=4, column=1, sticky="e", padx=3, pady=3)
        self.title_entry.grid(row=1, column=2, sticky="ew", padx=3, pady=3)
        self.desc_box.grid(row=3, column=2, rowspan=3, sticky="news", padx=3, pady=3)
        self.ingredients_frame.grid(row=0, column=2, sticky="nesw", padx=3, pady=3)

        if recipe.recipe_image != "None" and os.path.exists(recipe.recipe_image):
            try:
                self.display_image(True, recipe.recipe_image)
            except Exception as err:
                self.display_image(False)
                print(err)
        else:
            self.display_image(False)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=6)
        self.columnconfigure(2, weight=10)
        self.rowconfigure(0, weight=8)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

    def save_recipe(self):
        id_ = self.recipe_info.recipe_id
        name = self.tk_recipe_title.get()
        recipe_desc = self.desc_box.get("1.0", tk.END)

        if self.new_image is None:
            recipe_image = self.recipe_info.recipe_image
        else:
            recipe_image = self.new_image

        instructions_type = self.tk_recipe_instruc_type.get()
        if instructions_type == "file_location":
            recipe_instructions = self.tk_fileloc.get()
        else:
            recipe_instructions = self.tk_website_link.get()

        new_ingredient_list = []
        for index, row in enumerate(self.ingredients_frame.ingredients_row_widgets):
            ingredient: tk.StringVar = row[0]
            if index not in self.ingredients_frame.ignore:
                new_ingredient_list.append(ingredient.get())

        new_recipe = recipe_row(id_, name, new_ingredient_list, recipe_image, recipe_desc, recipe_instructions,
                                instructions_type, self.master_win.current_meal)
        self.master_win.recipes[id_] = new_recipe
        self.master_win.current_recipe = new_recipe
        self.recipe_info = new_recipe

    def back_button_command(self):
        self.save_recipe()
        self.master_win.swap_frame('Home Frame')

    def reset_button_command(self):
        self.master_win.swap_frame('Home Frame')
        self.master_win.swap_frame('Edit Frame')

    def select_file(self):
        new_path = filedialog.askopenfilename()
        self.tk_fileloc.set(new_path)

    def display_image(self, file_found, recipe_path=None):
        if file_found:
            recipe_image = Image.open(recipe_path)
            self.recipe_photo = ImageTk.PhotoImage(recipe_image)
            recipe_label = ttk.Label(self, image=self.recipe_photo)
            recipe_label.grid(row=0, column=0, columnspan=2)
        else:
            image_button = ttk.Button(self, text="select image", command=self.select_image)
            image_button.grid(row=0, column=0, columnspan=2)

    def select_image(self):
        image_path = filedialog.askopenfilename()
        try:
            self.display_image(True, image_path)
            self.new_image = image_path
        except Exception as err:
            print(err)


class IngredientsListFrame(ttk.Frame):
    def __init__(self, master: EditFrame):
        super().__init__(master)
        self.edit_frame = master
        self.ingredients_row_widgets: List[List[tk.StringVar | ttk.Entry | ttk.Button | ttk.Separator]] = []
        self.mini_frame = ttk.Frame(self)
        self.ignore = set()

        self.add_ingredient_button = ttk.Button(self, text="Add Ingredient", command=self.add_ingredient)
        ttk.Label(self, text="Ingredients", anchor="center").grid(row=0, column=1, columnspan=2, sticky="ew")

        self.mini_frame.columnconfigure(0, weight=5)
        self.mini_frame.columnconfigure(1, weight=2)
        for index, ingredient in enumerate(self.edit_frame.recipe_info.recipe_ingredients):
            self.ingredients_row_widgets.append([])
            self.ingredients_row_widgets[index].append(tk.StringVar(self.edit_frame.master_win, value=ingredient))
            ingredient_entry = ttk.Entry(self.mini_frame, textvariable=self.ingredients_row_widgets[index][0])
            self.ingredients_row_widgets[index].append(ingredient_entry)
            delete_button = ttk.Button(self.mini_frame, text="X", width=5, command=self.remove_ingredient(index))
            row_seperator = ttk.Separator(self.mini_frame)
            self.ingredients_row_widgets[index].append(delete_button)
            self.ingredients_row_widgets[index].append(row_seperator)

            next_row = index * 2
            ingredient_entry.grid(row=next_row, column=0, sticky="ew")
            delete_button.grid(row=next_row, column=1, sticky="w")
            row_seperator.grid(row=next_row+1, column=0, columnspan=2, sticky="ew")

            self.mini_frame.rowconfigure(next_row, weight=5)
            self.mini_frame.rowconfigure(next_row+1, weight=1)

        self.mini_frame.grid(row=1, column=0, columnspan=2, sticky="nesw")
        self.add_ingredient_button.grid(row=2, column=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.rowconfigure(2, weight=1)

        self.columnconfigure(0, weight=5)
        self.columnconfigure(1, weight=2)

    def add_ingredient(self):
        self.ingredients_row_widgets.append([])
        self.ingredients_row_widgets[-1].append(tk.StringVar(self.edit_frame.master_win))
        ingredient_entry = ttk.Entry(self.mini_frame, textvariable=self.ingredients_row_widgets[-1][0])
        self.ingredients_row_widgets[-1].append(ingredient_entry)
        delete_button = ttk.Button(self.mini_frame, text="X", width=5,
                                   command=self.remove_ingredient(len(self.ingredients_row_widgets) - 1))
        row_seperator = ttk.Separator(self.mini_frame)
        self.ingredients_row_widgets[-1].append(delete_button)
        self.ingredients_row_widgets[-1].append(row_seperator)

        next_row = len(self.ingredients_row_widgets) * 2
        ingredient_entry.grid(row=next_row, column=0, sticky="ew")
        delete_button.grid(row=next_row, column=1, sticky="w")
        row_seperator.grid(row=next_row + 1, column=0, columnspan=2, sticky="ew")

        self.mini_frame.rowconfigure(next_row, weight=5)
        self.mini_frame.rowconfigure(next_row + 1, weight=1)

    def remove_ingredient(self, index):
        def to_return():
            for widget in self.ingredients_row_widgets[index]:
                try:
                    widget.destroy()
                except AttributeError:
                    pass
                self.ignore.add(index)
        return to_return


class MealsFrame(ttk.Frame):
    def __init__(self, master: RecipesWindow):
        super().__init__(master)
        self.master_frame = master

        ttk.Label(self, text="Breakfast").grid(row=0, column=0)
        ttk.Label(self, text="Lunch").grid(row=0, column=1)
        ttk.Label(self, text="Dinner").grid(row=0, column=2)

        self.breakfast_random_button = ttk.Button(self, text="-> Random <-", command=self.random_breakfast)
        self.lunch_random_button = ttk.Button(self, text="-> Random <-", command=self.random_lunch)
        self.dinner_random_button = ttk.Button(self, text="-> Random <-", command=self.random_dinner)
        self.breakfast_random_button.grid(row=1, column=0)
        self.lunch_random_button.grid(row=1, column=1)
        self.dinner_random_button.grid(row=1, column=2)

        ttk.Separator(self).grid(row=2, column=0, columnspan=3, sticky="ew")

        self.breakfast_frame = MealDisplayColumn(self, self.master_frame.breakfast_recipe)
        self.lunch_frame = MealDisplayColumn(self, self.master_frame.lunch_recipe)
        self.dinner_frame = MealDisplayColumn(self, self.master_frame.dinner_recipe)
        self.breakfast_frame.grid(row=3, column=0, sticky='nesw')
        self.lunch_frame.grid(row=3, column=1, sticky='nesw')
        self.dinner_frame.grid(row=3, column=2, sticky='nesw')

        self.breakfast_open_button = ttk.Button(self, text="Open", command=self.breakfast_instructions)
        self.lunch_open_button = ttk.Button(self, text="Open", command=self.lunch_instructions)
        self.dinner_open_button = ttk.Button(self, text="Open", command=self.dinner_instructions)
        self.breakfast_open_button.grid(row=4, column=0)
        self.lunch_open_button.grid(row=4, column=1)
        self.dinner_open_button.grid(row=4, column=2)

        self.breakfast_edit_button = ttk.Button(self, text="Edit", command=self.edit_breakfast)
        self.lunch_edit_button = ttk.Button(self, text="Edit", command=self.edit_lunch)
        self.dinner_edit_button = ttk.Button(self, text="Edit", command=self.edit_dinner)
        self.breakfast_edit_button.grid(row=5, column=0)
        self.lunch_edit_button.grid(row=5, column=1)
        self.dinner_edit_button.grid(row=5, column=2)

        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=3)
        self.rowconfigure(2, weight=3)
        self.rowconfigure(3, weight=5)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def breakfast_instructions(self):
        open_instructions(self.master_frame.breakfast_recipe.recipe_id)

    def lunch_instructions(self):
        open_instructions(self.master_frame.lunch_recipe.recipe_id)

    def dinner_instructions(self):
        open_instructions(self.master_frame.dinner_recipe.recipe_id)

    def edit_breakfast(self):
        self.master_frame.current_meal = "breakfast"
        self.master_frame.recipes = self.master_frame.breakfasts
        self.master_frame.current_recipe = self.master_frame.breakfast_recipe
        self.master_frame.swap_frame('Home Frame')

    def edit_lunch(self):
        self.master_frame.current_meal = "lunch"
        self.master_frame.recipes = self.master_frame.lunches
        self.master_frame.current_recipe = self.master_frame.lunch_recipe
        self.master_frame.swap_frame('Home Frame')

    def edit_dinner(self):
        self.master_frame.current_meal = "dinner"
        self.master_frame.recipes = self.master_frame.dinners
        self.master_frame.current_recipe = self.master_frame.dinner_recipe
        self.master_frame.swap_frame('Home Frame')

    def random_breakfast(self):
        options = list(self.master_frame.breakfasts.values())
        options.remove(self.master_frame.breakfast_recipe)
        if options:
            new_recipe = choice(options)
            self.breakfast_frame.destroy()
            self.master_frame.breakfast_recipe = new_recipe
            self.breakfast_frame = MealDisplayColumn(self, new_recipe)
            self.breakfast_frame.grid(row=3, column=0, sticky='nesw')

    def random_lunch(self):
        options = list(self.master_frame.lunches.values())
        options.remove(self.master_frame.lunch_recipe)
        if options:
            new_recipe = choice(options)
            self.lunch_frame.destroy()
            self.master_frame.lunch_recipe = new_recipe
            self.lunch_frame = MealDisplayColumn(self, new_recipe)
            self.lunch_frame.grid(row=3, column=1, sticky='nesw')

    def random_dinner(self):
        options = list(self.master_frame.dinners.values())
        options.remove(self.master_frame.dinner_recipe)
        if options:
            new_recipe = choice(options)
            self.dinner_frame.destroy()
            self.master_frame.dinner_recipe = new_recipe
            self.dinner_frame = MealDisplayColumn(self, new_recipe)
            self.dinner_frame.grid(row=3, column=0, sticky='nesw')


class MealDisplayColumn(ttk.Frame):
    def __init__(self, master: MealsFrame, recipe: recipe_row):
        super().__init__(master)
        self.recipe_label = ttk.Label(self, text=recipe.recipe_name)
        self.recipe_label.grid(row=0, column=0, sticky="s")

        self.recipe_photo = None
        self.new_image = None
        self.display_image(os.path.exists(recipe.recipe_image), recipe.recipe_image)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.columnconfigure(0, weight=1)

    def display_image(self, file_found, recipe_path=None):
        try:
            if file_found:
                recipe_image = Image.open(recipe_path)
                self.recipe_photo = ImageTk.PhotoImage(recipe_image)
                recipe_label = ttk.Label(self, image=self.recipe_photo)
                recipe_label.grid(row=1, column=0)
            else:
                image_button = ttk.Button(self, text="select image", command=self.select_image)
                image_button.grid(row=1, column=0)
        except Exception as err:
            print(err)

    def select_image(self):
        image_path = filedialog.askopenfilename()
        try:
            self.display_image(True, image_path)
            self.new_image = image_path
        except Exception as err:
            print(err)
