# -*- coding: utf-8 -*-
"""
Created on Mon Sep 29 17:39:23 2025

@author: 11728
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
import random

class DoubleColorBallSimulator:
    def __init__(self):
        self.prize_pool = 0
        self.history = []
        self.my_balance = 0
        self.my_tickets = 0
        self.current_period = 0
        self.selected_reds = []
        self.selected_blues = []
    
    def generate_ticket(self):
        red_balls = random.sample(range(1, 34), 6)
        blue_ball = random.randint(1, 16)
        return sorted(red_balls), blue_ball
    
    def check_prize(self, my_red, my_blue, prize_red, prize_blue):
        red_match = len(set(my_red) & set(prize_red))
        blue_match = my_blue == prize_blue
        
        if red_match == 6 and blue_match:
            return "一等奖", 6000000
        elif red_match == 6:
            return "二等奖", 200000
        elif red_match == 5 and blue_match:
            return "三等奖", 3000
        elif red_match == 5 or (red_match == 4 and blue_match):
            return "四等奖", 200
        elif red_match == 4 or (red_match == 3 and blue_match):
            return "五等奖", 10
        elif blue_match:
            return "六等奖", 5
        else:
            return "未中奖", 0
    
    def simulate_draw(self, custom_reds=None, custom_blues=None):
        self.current_period += 1
        prize_red, prize_blue = self.generate_ticket()
        
        if custom_reds and custom_blues:
            # 复式投注逻辑
            from itertools import combinations
            tickets = []
            red_combinations = list(combinations(custom_reds, 6))
            for red_combo in red_combinations:
                for blue in custom_blues:
                    tickets.append((list(red_combo), blue))
            
            total_cost = len(tickets) * 2
            total_prize = 0
            best_prize_level = "未中奖"
            
            for my_red, my_blue in tickets:
                prize_level, prize_amount = self.check_prize(my_red, my_blue, prize_red, prize_blue)
                total_prize += prize_amount
                if prize_amount > 0 and self.get_prize_rank(prize_level) > self.get_prize_rank(best_prize_level):
                    best_prize_level = prize_level
            
            self.my_balance += total_prize - total_cost
            self.my_tickets += len(tickets)
            
            result = {
                "期数": self.current_period,
                "开奖红球": prize_red,
                "开奖蓝球": prize_blue,
                "我的红球": custom_reds,
                "我的蓝球": custom_blues,
                "中奖情况": f"复式({len(tickets)}注)",
                "奖金": total_prize,
                "累计收益": self.my_balance,
                "注数": len(tickets)
            }
        else:
            # 单式投注
            my_red, my_blue = self.generate_ticket()
            prize_level, prize_amount = self.check_prize(my_red, my_blue, prize_red, prize_blue)
            self.prize_pool += 12000000
            self.my_balance += prize_amount - 2
            self.my_tickets += 1
            
            result = {
                "期数": self.current_period,
                "开奖红球": prize_red,
                "开奖蓝球": prize_blue,
                "我的红球": my_red,
                "我的蓝球": my_blue,
                "中奖情况": prize_level,
                "奖金": prize_amount,
                "累计收益": self.my_balance,
                "注数": 1
            }
        
        self.history.append(result)
        return result
    
    def get_prize_rank(self, prize_level):
        ranks = {"一等奖": 7, "二等奖": 6, "三等奖": 5, "四等奖": 4, "五等奖": 3, "六等奖": 2, "未中奖": 1}
        return ranks.get(prize_level, 1)

class LotteryApp(App):
    def build(self):
        self.simulator = DoubleColorBallSimulator()
        self.title = "双色球模拟器"
        
        # 创建主布局
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 创建选项卡
        self.tabs = TabbedPanel()
        self.tabs.do_default_tab = False
        
        # 模拟控制选项卡
        control_tab = TabbedPanelItem(text='模拟控制')
        control_layout = BoxLayout(orientation='vertical', spacing=10)
        
        # 随机投注按钮
        random_buttons = BoxLayout(spacing=10, size_hint_y=0.2)
        random_buttons.add_widget(Button(text='模拟1期', on_press=self.simulate_one))
        random_buttons.add_widget(Button(text='模拟10期', on_press=lambda x: self.simulate_multiple(10)))
        random_buttons.add_widget(Button(text='模拟100期', on_press=lambda x: self.simulate_multiple(100)))
        control_layout.add_widget(random_buttons)
        
        # 结果显示区域
        self.result_display = TextInput(
            text='欢迎使用双色球模拟器！\n点击按钮开始模拟...\n',
            size_hint_y=0.7,
            readonly=True,
            background_color=[1, 1, 1, 1]
        )
        control_layout.add_widget(self.result_display)
        
        # 工具按钮
        tool_buttons = BoxLayout(spacing=10, size_hint_y=0.1)
        tool_buttons.add_widget(Button(text='显示统计', on_press=self.show_stats))
        tool_buttons.add_widget(Button(text='重置模拟', on_press=self.reset_simulation))
        control_layout.add_widget(tool_buttons)
        
        control_tab.add_widget(control_layout)
        self.tabs.add_widget(control_tab)
        
        # 号码选择选项卡
        select_tab = TabbedPanelItem(text='号码选择')
        select_layout = BoxLayout(orientation='vertical', spacing=10)
        
        # 红球选择
        red_label = Label(text='选择红球 (至少6个):', size_hint_y=0.1)
        select_layout.add_widget(red_label)
        
        red_scroll = ScrollView(size_hint_y=0.4)
        red_grid = GridLayout(cols=6, spacing=5, size_hint_y=None)
        red_grid.bind(minimum_height=red_grid.setter('height'))
        
        self.red_buttons = []
        for i in range(1, 34):
            btn = Button(text=str(i), size_hint_y=None, height=60)
            btn.bind(on_press=lambda x, num=i: self.toggle_red(num))
            red_grid.add_widget(btn)
            self.red_buttons.append(btn)
        
        red_scroll.add_widget(red_grid)
        select_layout.add_widget(red_scroll)
        
        # 蓝球选择
        blue_label = Label(text='选择蓝球 (至少1个):', size_hint_y=0.1)
        select_layout.add_widget(blue_label)
        
        blue_grid = GridLayout(cols=8, spacing=5, size_hint_y=0.2)
        self.blue_buttons = []
        for i in range(1, 17):
            btn = Button(text=str(i), size_hint_y=None, height=60)
            btn.bind(on_press=lambda x, num=i: self.toggle_blue(num))
            blue_grid.add_widget(btn)
            self.blue_buttons.append(btn)
        
        select_layout.add_widget(blue_grid)
        
        # 选择信息
        self.selection_info = Label(text='当前选择: 红球: 0个, 蓝球: 0个', size_hint_y=0.1)
        select_layout.add_widget(self.selection_info)
        
        # 自选投注按钮
        custom_buttons = BoxLayout(spacing=10, size_hint_y=0.1)
        custom_buttons.add_widget(Button(text='使用自选号码模拟1期', on_press=self.simulate_custom))
        custom_buttons.add_widget(Button(text='机选一注', on_press=self.quick_select))
        custom_buttons.add_widget(Button(text='清空选择', on_press=self.clear_selection))
        select_layout.add_widget(custom_buttons)
        
        select_tab.add_widget(select_layout)
        self.tabs.add_widget(select_tab)
        
        main_layout.add_widget(self.tabs)
        return main_layout
    
    def toggle_red(self, number):
        if number in self.simulator.selected_reds:
            self.simulator.selected_reds.remove(number)
            self.red_buttons[number-1].background_color = [1, 1, 1, 1]  # 白色
        else:
            self.simulator.selected_reds.append(number)
            self.red_buttons[number-1].background_color = [1, 0, 0, 1]  # 红色
        self.update_selection_info()
    
    def toggle_blue(self, number):
        if number in self.simulator.selected_blues:
            self.simulator.selected_blues.remove(number)
            self.blue_buttons[number-1].background_color = [1, 1, 1, 1]  # 白色
        else:
            self.simulator.selected_blues.append(number)
            self.blue_buttons[number-1].background_color = [0, 0, 1, 1]  # 蓝色
        self.update_selection_info()
    
    def update_selection_info(self):
        red_count = len(self.simulator.selected_reds)
        blue_count = len(self.simulator.selected_blues)
        self.selection_info.text = f'当前选择: 红球: {red_count}个, 蓝球: {blue_count}个'
    
    def quick_select(self):
        self.clear_selection()
        reds = random.sample(range(1, 34), 6)
        blue = random.randint(1, 16)
        for red in reds:
            self.toggle_red(red)
        self.toggle_blue(blue)
    
    def clear_selection(self):
        self.simulator.selected_reds.clear()
        self.simulator.selected_blues.clear()
        for btn in self.red_buttons:
            btn.background_color = [1, 1, 1, 1]
        for btn in self.blue_buttons:
            btn.background_color = [1, 1, 1, 1]
        self.update_selection_info()
    
    def simulate_one(self, instance):
        result = self.simulator.simulate_draw()
        self.display_result(result)
    
    def simulate_multiple(self, periods):
        for i in range(periods):
            result = self.simulator.simulate_draw()
            if result["中奖情况"] != "未中奖" or (i + 1) % 10 == 0:
                self.display_result(result)
    
    def simulate_custom(self, instance):
        if len(self.simulator.selected_reds) < 6 or len(self.simulator.selected_blues) < 1:
            self.result_display.text += "\n错误：请至少选择6个红球和1个蓝球！\n"
            return
        
        result = self.simulator.simulate_draw(self.simulator.selected_reds, self.simulator.selected_blues)
        self.display_result(result)
    
    def display_result(self, result):
        if "复式" in result["中奖情况"]:
            output = (f"第{result['期数']}期: "
                     f"开奖{result['开奖红球']}+[{result['开奖蓝球']}] | "
                     f"我的{result['我的红球']}+{result['我的蓝球']} | "
                     f"{result['中奖情况']} | "
                     f"奖金:{result['奖金']}元 | "
                     f"累计:{result['累计收益']}元\n")
        else:
            output = (f"第{result['期数']}期: "
                     f"开奖{result['开奖红球']}+[{result['开奖蓝球']}] | "
                     f"我的{result['我的红球']}+[{result['我的蓝球']}] | "
                     f"{result['中奖情况']} | "
                     f"奖金:{result['奖金']}元 | "
                     f"累计:{result['累计收益']}元\n")
        
        self.result_display.text += output
    
    def reset_simulation(self, instance):
        self.simulator = DoubleColorBallSimulator()
        self.result_display.text = "模拟已重置！\n欢迎使用双色球模拟器！\n"
    
    def show_stats(self, instance):
        if not self.simulator.history:
            self.result_display.text += "\n还没有进行模拟！\n"
            return
        
        total_prize = sum(r["奖金"] for r in self.simulator.history)
        total_tickets = sum(r.get("注数", 1) for r in self.simulator.history)
        winning_tickets = len([r for r in self.simulator.history if r["奖金"] > 0])
        total_periods = len(self.simulator.history)
        
        stats = (f"\n=== 统计信息 ===\n"
                f"模拟期数: {total_periods}\n"
                f"总注数: {total_tickets}注\n"
                f"总奖金: {total_prize}元\n"
                f"净收益: {self.simulator.my_balance}元\n"
                f"中奖率: {winning_tickets/total_periods*100:.1f}%\n")
        
        self.result_display.text += stats

if __name__ == '__main__':
    LotteryApp().run()