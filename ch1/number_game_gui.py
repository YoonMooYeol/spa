import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'

import random as rd
import tkinter as tk
from tkinter import messagebox

class NumberGuessingGameGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("숫자 맞추기 게임")
        self.window.geometry("400x500")
        self.window.configure(bg='#f0f0f0')
        
        # 게임 설정
        self.MIN_NUMBER = 1
        self.MAX_NUMBER = 10
        self.random_number = 0
        self.game_started = False
        
        self.setup_gui()
        
    def setup_gui(self):
        # 제목
        title_label = tk.Label(
            self.window,
            text="숫자 맞추기 게임",
            font=("맑은 고딕", 24, "bold"),
            bg='#f0f0f0',
            pady=20
        )
        title_label.pack()
        
        # 게임 컨테이너
        self.game_frame = tk.Frame(self.window, bg='#f0f0f0')
        self.game_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # 안내 메시지
        self.instruction_label = tk.Label(
            self.game_frame,
            text=f"{self.MIN_NUMBER}부터 {self.MAX_NUMBER} 사이의 숫자를 맞춰보세요!",
            font=("맑은 고딕", 12),
            bg='#f0f0f0'
        )
        self.instruction_label.pack(pady=10)
        
        # 입력 필드
        self.entry = tk.Entry(
            self.game_frame,
            font=("맑은 고딕", 14),
            width=10,
            justify='center',
            bd=2,
            relief='solid'
        )
        self.entry.pack(pady=20)
        
        # 결과 메시지 (더 크게 표시)
        self.result_label = tk.Label(
            self.game_frame,
            text="Enter 키를 누르면 게임이 시작됩니다!",
            font=("맑은 고딕", 13),
            bg='#f0f0f0',
            wraplength=350,
            height=3  # 3줄 높이 확보
        )
        self.result_label.pack(pady=20)
        
        # Enter 키 바인딩
        self.entry.bind('<Return>', lambda event: self.check_guess())
        
        # 초기 게임 시작
        self.start_game()
        
    def start_game(self):
        """게임을 시작합니다."""
        self.random_number = rd.randint(self.MIN_NUMBER, self.MAX_NUMBER)
        self.game_started = True
        self.entry.delete(0, tk.END)
        self.result_label.config(text="숫자를 입력하고 Enter 키를 누르세요!")
        self.entry.focus()
        
    def check_guess(self):
        """사용자의 추측을 확인합니다."""
        if not self.game_started:
            self.start_game()
            return
            
        guess = self.entry.get().strip()
        self.entry.delete(0, tk.END)
        
        try:
            guess = int(guess)
            if not (self.MIN_NUMBER <= guess <= self.MAX_NUMBER):
                raise ValueError
        except ValueError:
            self.result_label.config(
                text=f"잘못된 입력입니다!\n{self.MIN_NUMBER}부터 {self.MAX_NUMBER} 사이의 숫자만 입력해주세요.",
                fg='red'
            )
            return
        
        if guess == self.random_number:
            self.result_label.config(
                text=f"🎉 정답입니다! {self.random_number}를 맞추셨습니다! 🎉\nEnter 키를 누르면 새 게임이 시작됩니다.",
                fg='green'
            )
            self.game_started = False
        elif guess < self.random_number:
            self.result_label.config(text="더 큰 숫자입니다! ⬆️", fg='blue')
        else:
            self.result_label.config(text="더 작은 숫자입니다! ⬇️", fg='blue')
            
        self.entry.focus()
                
    def run(self):
        """게임을 실행합니다."""
        self.entry.focus()
        self.window.mainloop()

if __name__ == "__main__":
    game = NumberGuessingGameGUI()
    game.run()
