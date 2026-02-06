#!python
"""
eat-food 真实热量计算器
基于《中国食物成分表》标准数据
"""

import json
import os

class RealCalorieCalculator:
    def __init__(self):
        # 中国常见食物真实热量数据（单位：千卡/100g可食部）
        self.food_data = {
            # 谷薯类
            "大米": {"calories": 346, "protein": 7.4, "fat": 0.8, "carbs": 77.2},
            "米饭": {"calories": 116, "protein": 2.6, "fat": 0.3, "carbs": 25.6},
            "面条": {"calories": 284, "protein": 8.3, "fat": 0.7, "carbs": 61.9},
            "馒头": {"calories": 223, "protein": 7.0, "fat": 1.1, "carbs": 47.0},
            "面包": {"calories": 312, "protein": 8.3, "fat": 5.1, "carbs": 58.6},
            
            # 肉蛋类
            "鸡蛋": {"calories": 144, "protein": 13.3, "fat": 8.8, "carbs": 2.8},
            "鸡胸肉": {"calories": 133, "protein": 19.4, "fat": 5.0, "carbs": 2.5},
            "鸡腿": {"calories": 181, "protein": 16.0, "fat": 13.0, "carbs": 0},
            "猪肉": {"calories": 395, "protein": 13.2, "fat": 37.0, "carbs": 2.4},
            "牛肉": {"calories": 125, "protein": 19.9, "fat": 4.2, "carbs": 2.0},
            "鱼": {"calories": 113, "protein": 20.0, "fat": 3.4, "carbs": 0},
            
            # 蔬菜类
            "番茄": {"calories": 19, "protein": 0.9, "fat": 0.2, "carbs": 4.0},
            "黄瓜": {"calories": 15, "protein": 0.8, "fat": 0.2, "carbs": 2.9},
            "白菜": {"calories": 17, "protein": 1.5, "fat": 0.1, "carbs": 3.2},
            "土豆": {"calories": 77, "protein": 2.0, "fat": 0.2, "carbs": 17.2},
            "胡萝卜": {"calories": 37, "protein": 1.0, "fat": 0.2, "carbs": 8.8},
            
            # 豆制品
            "豆腐": {"calories": 81, "protein": 8.1, "fat": 3.7, "carbs": 4.2},
            "豆浆": {"calories": 14, "protein": 1.8, "fat": 0.7, "carbs": 1.1},
            
            # 水果
            "苹果": {"calories": 52, "protein": 0.2, "fat": 0.2, "carbs": 13.5},
            "香蕉": {"calories": 89, "protein": 1.1, "fat": 0.3, "carbs": 22.0},
            "橙子": {"calories": 47, "protein": 0.8, "fat": 0.2, "carbs": 11.7},
            
            # 调料
            "食用油": {"calories": 899, "protein": 0, "fat": 99.9, "carbs": 0},
            "白糖": {"calories": 400, "protein": 0, "fat": 0, "carbs": 99.9},
            "盐": {"calories": 0, "protein": 0, "fat": 0, "carbs": 0},
        }
    
    def calculate_meal(self, meal_items):
        """计算一餐的营养成分"""
        total = {
            "calories": 0,      # 总热量（千卡）
            "protein": 0,       # 蛋白质（克）
            "fat": 0,           # 脂肪（克）
            "carbs": 0,         # 碳水化合物（克）
            "foods": []         # 详细记录
        }
        
        print("\n" + "="*50)
        print("🍽️  真实热量计算器 - 基于《中国食物成分表》")
        print("="*50)
        
        for food_name, grams in meal_items.items():
            food_name = food_name.strip()
            
            # 查找食物（支持中文名）
            found = False
            for food_key, nutrients in self.food_data.items():
                if food_key == food_name:
                    calories = nutrients["calories"] * grams / 100
                    protein = nutrients["protein"] * grams / 100
                    fat = nutrients["fat"] * grams / 100
                    carbs = nutrients["carbs"] * grams / 100
                    
                    total["calories"] += calories
                    total["protein"] += protein
                    total["fat"] += fat
                    total["carbs"] += carbs
                    
                    food_info = {
                        "name": food_name,
                        "grams": grams,
                        "calories": round(calories, 1),
                        "protein": round(protein, 1),
                        "fat": round(fat, 1),
                        "carbs": round(carbs, 1)
                    }
                    total["foods"].append(food_info)
                    
                    print(f"📝 {food_name}: {grams}g")
                    print(f"   🔥 {calories:.1f}千卡 | 🥚 {protein:.1f}g蛋白 | 🥑 {fat:.1f}g脂肪 | 🍚 {carbs:.1f}g碳水")
                    found = True
                    break
            
            if not found:
                print(f"⚠️  未找到数据: {food_name} (已跳过)")
        
        print("-"*50)
        print("📊 营养总计:")
        print(f"   总热量: {total['calories']:.1f} 千卡")
        print(f"   蛋白质: {total['protein']:.1f}g")
        print(f"   脂肪: {total['fat']:.1f}g")
        print(f"   碳水化合物: {total['carbs']:.1f}g")
        
        # 计算热量占比
        if total["calories"] > 0:
            protein_kcal = total["protein"] * 4
            fat_kcal = total["fat"] * 9
            carbs_kcal = total["carbs"] * 4
            
            protein_pct = (protein_kcal / total["calories"]) * 100
            fat_pct = (fat_kcal / total["calories"]) * 100
            carbs_pct = (carbs_kcal / total["calories"]) * 100
            
            print("\n📈 热量来源比例:")
            print(f"   蛋白质: {protein_pct:.1f}% ({protein_kcal:.1f}千卡)")
            print(f"   脂肪: {fat_pct:.1f}% ({fat_kcal:.1f}千卡)")
            print(f"   碳水: {carbs_pct:.1f}% ({carbs_kcal:.1f}千卡)")
        
        # 健康建议
        print("\n💡 健康建议:")
        if protein_pct < 15:
            print("   ⚠️  蛋白质摄入偏低，建议增加蛋、肉、豆制品")
        elif protein_pct > 35:
            print("   ⚠️  蛋白质摄入偏高，注意肾脏负担")
        else:
            print("   ✅ 蛋白质摄入比例合理")
        
        if fat_pct > 30:
            print("   ⚠️  脂肪摄入偏高，建议减少油炸食品")
        
        print("="*50)
        
        # 保存结果
        self.save_result(total)
        return total
    
    def save_result(self, result):
        """保存计算结果到文件"""
        try:
            with open("calorie_result.txt", "a", encoding="utf-8") as f:
                from datetime import datetime
                f.write(f"\n{'='*40}\n")
                f.write(f"记录时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
                f.write(f"总热量: {result['calories']:.1f}千卡\n")
                for food in result["foods"]:
                    f.write(f"{food['name']}: {food['grams']}g = {food['calories']:.1f}千卡\n")
            print("💾 结果已保存到 calorie_result.txt")
        except:
            print("💾 结果保存失败")

def main():
    calculator = RealCalorieCalculator()
    
    # 示例：一顿正常的午餐
    print("示例：一顿午餐的热量计算")
    lunch = {
        "米饭": 200,      # 200克米饭
        "鸡胸肉": 150,    # 150克鸡胸肉
        "番茄": 100,      # 100克番茄
        "黄瓜": 100,      # 100克黄瓜
        "食用油": 10,     # 10克油（约1汤匙）
    }
    
    calculator.calculate_meal(lunch)
    
    # 交互模式
    print("\n🎮 开始自定义计算（输入'q'退出）")
    while True:
        try:
            food = input("\n请输入食物名称（中文）: ").strip()
            if food.lower() == 'q':
                break
            
            if food not in calculator.food_data:
                print(f"⚠️  未知食物，可用食物: {', '.join(list(calculator.food_data.keys())[:10])}...")
                continue
            
            grams = float(input(f"请输入{food}的重量(克): "))
            
            calculator.calculate_meal({food: grams})
            
        except ValueError:
            print("⚠️  请输入有效的数字")
        except KeyboardInterrupt:
            print("\n👋 再见！")
            break

if __name__ == "__main__":
    main()