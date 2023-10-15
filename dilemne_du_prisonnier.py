import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random as random

class AppDilemn:
    def __init__(self) -> None:
        self.fenetre = tk.Tk()
        self.fenetre.title("Dilemne du prisonnier")
        self.fenetre.configure(bg='black')
        self.fenetre.geometry("1920x1080")

        self.current_game = Game()
        self.make_imgs()
        self.make_widgets()

        self.win_number = 0
        self.lose_number = 0
        self.total_number = 0

        self.delay_chart = 20
    
    def make_chart(self):
        labels = 'Victoires', 'Défaites'
        sizes = [self.win_number, self.lose_number]
        fig = plt.Figure(figsize=(5, 4), dpi=100)
        self.ax = fig.add_subplot(111)
        self.ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        canvas = FigureCanvasTkAgg(fig, master=self.fenetre)
        canvas.draw()
        canvas.get_tk_widget().grid(row=3, column=1)
    
    def update_chart(self):
        self.ax.clear()
        labels = 'Victoires', 'Défaites'
        sizes = [self.win_number, self.lose_number]
        fig = plt.Figure(figsize=(5, 4), dpi=100)
        self.ax = fig.add_subplot(111)
        self.ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        canvas = FigureCanvasTkAgg(fig, master=self.fenetre)
        canvas.draw()
        canvas.get_tk_widget().grid(row=3, column=1)

    def make_imgs(self):
        self.img_closed_door = tk.PhotoImage(file = 'imgs/closed_door.png')
        self.img_closed_door = self.img_closed_door.subsample(2)
        self.img_openned_door_car = tk.PhotoImage(file = 'imgs/openned_door_with_car.png')
        self.img_openned_door_car = self.img_openned_door_car.subsample(2)
        self.img_openned_dor_no_car = tk.PhotoImage(file = 'imgs/openned_door_without_car.png')
        self.img_openned_dor_no_car = self.img_openned_dor_no_car.subsample(2)
        self.img_selected_closed_door = tk.PhotoImage(file = 'imgs/selected_closed_door.png')
        self.img_selected_closed_door = self.img_selected_closed_door.subsample(2)

    def make_widgets(self):
        self.button_left = tk.Button(self.fenetre, image=self.img_closed_door, relief=tk.FLAT, command=self.select_left_door, border=0, bg='black')
        self.button_center = tk.Button(self.fenetre, image=self.img_closed_door, relief=tk.FLAT, command = self.select_center_door,bg='black')
        self.button_right = tk.Button(self.fenetre, image=self.img_closed_door, relief=tk.FLAT, command = self.select_right_door,bg='black')
        self.button_left.grid(row=0, column=0, padx=220)
        self.button_center.grid(row=0, column=1, padx=220)
        self.button_right.grid(row=0, column=2, padx=220)
        self.instruction_text = tk.Label(self.fenetre, text="Veuillez selectionner une porte.", font=("Helvetica", 20), background='black', fg='white')
        self.instruction_text.grid(row=1, column=1, pady=100)    
        self.doors = {'left_door':self.button_left, 'center_door':self.button_center, 'right_door':self.button_right}
        self.restart_button = tk.Button(self.fenetre, text='Recommencer', width=20, command=self.restart_game)
        self.restart_button.grid(row=2, column=1, pady=5) 
        self.button_win_simulation = tk.Button(text="Simuler stratégie gagnante", command=self.simulate_win_strategy_p1, background='black', fg='green')
        self.button_win_simulation.grid(row=2,column=0)
        self.button_lose_simulation = tk.Button(text="Simuler stratégie perdante", command=self.simulate_lose_strategy_p1, background='black', fg='red')
        self.button_lose_simulation.grid(row=2,column=2)

    def select_door(self,door):
        if self.current_game.round_number == 0:
            self.showed_door = self.current_game.find_door_to_open_first_round(door)
            button = self.doors[self.showed_door]
            button.configure(image = self.img_openned_dor_no_car) 
            self.doors[door].configure(image=self.img_selected_closed_door)
            self.door_to_select = self.get_door_to_open_winning_strategy(self.showed_door, door)
            self.round_switch()
        elif self.current_game.round_number == 1:
            self.check_round_win(door)

    def get_door_to_open_winning_strategy(self, showed_door, selected_door):
        L = self.current_game.doors
        L.remove(showed_door)
        L.remove(selected_door)
        return(L[0])
    
    def select_left_door(self):
        self.select_door('left_door')
    def select_center_door(self):
        self.select_door('center_door')
    def select_right_door(self):
        self.select_door('right_door')
    
    def round_switch(self):
        self.instruction_text.configure(text= "Vous avez l'occasion de choisir une nouvelle porte.")

    def check_round_win(self, door):
        if self.current_game.check_win_second_round(door):
            self.instruction_text.configure(text= "Vous avez gagné !")
            self.instruction_text.configure(fg='green')
            self.doors[door].configure(image=self.img_openned_door_car)
            self.win_number+=1
            if self.total_number==0:
                self.make_chart()
            else:
                self.update_chart()
            self.total_number+=1

        else:
            self.instruction_text.configure(text= "Vous avez perdu !")
            self.instruction_text.configure(fg='red')
            self.doors[door].configure(image=self.img_openned_dor_no_car)
            self.doors[self.current_game.good_door].configure(image=self.img_openned_door_car)
            self.lose_number+=1
            if self.total_number==0:
                self.make_chart()
            else:
                self.update_chart()
            self.total_number+=1
        
    def restart_game(self):
        self.current_game = Game()
        self.button_left.configure(image = self.img_closed_door)
        self.button_right.configure(image = self.img_closed_door)
        self.button_center.configure(image = self.img_closed_door)
        self.instruction_text.configure(text="Veuillez selectionner une porte")
        self.instruction_text.configure(fg='white')
        print(self.total_number)
    
    def simulate_lose_strategy_p1(self):
            self.restart_game()
            self.fenetre.after(self.delay_chart, self.simulate_lose_strategy_p2)

    def simulate_lose_strategy_p2(self):
            self.select_left_door()
            self.fenetre.after(self.delay_chart, self.simulate_lose_strategy_p3)
    
    def simulate_lose_strategy_p3(self):
            self.select_left_door()
            self.fenetre.after(self.delay_chart, self.simulate_lose_strategy_p1)
        

    def simulate_win_strategy_p1(self):
            self.restart_game()
            self.fenetre.after(self.delay_chart, self.simulate_win_strategy_p2)

    def simulate_win_strategy_p2(self):
            self.select_left_door()
            self.fenetre.after(self.delay_chart, self.simulate_win_strategy_p3)

    def simulate_win_strategy_p3(self):
            self.select_door(self.door_to_select)
            self.fenetre.after(self.delay_chart, self.simulate_win_strategy_p1)
            

    
class Game():
    def __init__(self) -> None:
        self.doors = ['left_door', 'center_door', 'right_door']
        self.good_door = self.doors[random.randint(0,2)]
        self.wrong_doors = [i for i in self.doors]
        self.wrong_doors.remove(self.good_door)
        self.round_number = 0
        self.game_status = 'pending'

    def find_door_to_open_first_round(self, selected_door):
        self.round_number+=1
        if selected_door in self.wrong_doors:
            L = self.wrong_doors
            L.remove(selected_door)
            return(L[0])
        else:
            return(self.wrong_doors[random.randint(0,1)])
            
    def check_win_second_round(self, selected_door):
        if selected_door==self.good_door:
            self.game_status = 'won'
            return(True)
        
        else: 
            self.game_status = 'lost'
            return(False)
    
if __name__=="__main__":
    app = AppDilemn()
    app.fenetre.mainloop()
    game_test_backend = Game()
