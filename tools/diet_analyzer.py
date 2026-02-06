#!python
"""
饮食分析报告生成器
分析一日三餐的营养状况
"""

import json
from datetime import datetime, timedelta

class DietAnalyzer:
    def __init__(self):
        # 中国居民膳食营养素参考摄入量（成人）
        self.daily_reference = {
            "calories": 2250,      # 千卡（轻体力活动男性）
            "protein": 65,         # 克
            "fat": {               # 脂肪供能比20%-30%
                "min": 2250 * 0.2 / 9,  # 最小脂肪克数
                "max": 2250 * 0.3 / 9,  # 最大脂肪克数
            },
            "carbs": 300,          # 克
            "fiber": 25,           # 膳食纤维（克）
            "calcium": 800,        # 钙（毫克）
            "iron": 12,            # 铁（毫克）
            "vitamin_c": 100,      # 维生素C（毫克）
        }
        
        # 食物营养数据库（简略版）
        self.nutrient_db = {
            "米饭": {"calories": 116, "protein": 2.6, "fat": 0.3, "carbs": 25.6, "fiber": 0.3},
            "鸡蛋": {"calories": 144, "protein": 13.3, "fat": 8.8, "carbs": 2.8, "fiber": 0},
            "番茄": {"calories": 19, "protein": 0.9, "fat": 0.2, "carbs": 4.0, "fiber": 0.5},
            "鸡胸肉": {"calories": 133, "protein": 19.4, "fat": 5.0, "carbs": 2.5, "fiber": 0},
            "牛奶": {"calories": 54, "protein": 3.0, "fat": 3.2, "carbs": 3.4, "fiber": 0, "calcium": 104},
            "菠菜": {"calories": 28, "protein": 2.6, "fat": 0.3, "carbs": 4.5, "fiber": 1.7, "iron": 2.9, "vitamin_c": 32},
        }
    
    def analyze_day(self, meals):
        """分析一天的饮食"""
        daily_total = {
            "calories": 0, "protein": 0, "fat": 0, "carbs": 0,
            "fiber": 0, "calcium": 0, "iron": 0, "vitamin_c": 0
        }
        
        print("\n" + "="*60)
        print("📊 饮食分析报告")
        print("="*60)
        
        # 分析每餐
        meal_results = {}
        for meal_type, meal_items in meals.items():
            print(f"\n🍽️  {meal_type}:")
            print("-"*40)
            
            meal_total = {"calories": 0, "protein": 0, "fat": 0, "carbs": 0}
            
            for food_item in meal_items:
                food_name = food_item.get("name", "")
                grams = food_item.get("grams", 0)
                
                if food_name in self.nutrient_db:
                    nutrients = self.nutrient_db[food_name]
                    
                    # 计算营养值
                    calories = nutrients.get("calories", 0) * grams / 100
                    protein = nutrients.get("protein", 0) * grams / 100
                    fat = nutrients.get("fat", 0) * grams / 100
                    carbs = nutrients.get("carbs", 0) * grams / 100
                    fiber = nutrients.get("fiber", 0) * grams / 100
                    calcium = nutrients.get("calcium", 0) * grams / 100
                    iron = nutrients.get("iron", 0) * grams / 100
                    vitamin_c = nutrients.get("vitamin_c", 0) * grams / 100
                    
                    # 累加
                    meal_total["calories"] += calories
                    meal_total["protein"] += protein
                    meal_total["fat"] += fat
                    meal_total["carbs"] += carbs
                    
                    daily_total["calories"] += calories
                    daily_total["protein"] += protein
                    daily_total["fat"] += fat
                    daily_total["carbs"] += carbs
                    daily_total["fiber"] += fiber
                    daily_total["calcium"] += calcium
                    daily_total["iron"] += iron
                    daily_total["vitamin_c"] += vitamin_c
                    
                    print(f"  {food_name}: {grams}g")
                    print(f"    → {calories:.0f}千卡")
                else:
                    print(f"  ⚠️  {food_name}: 营养数据未知")
            
            meal_results[meal_type] = meal_total
            
            # 显示每餐总计
            print(f"\n  📈 本餐总计:")
            print(f"    热量: {meal_total['calories']:.0f}千卡")
            print(f"    蛋白质: {meal_total['protein']:.1f}g")
            print(f"    脂肪: {meal_total['fat']:.1f}g")
            print(f"    碳水: {meal_total['carbs']:.1f}g")
        
        # 显示全天总计
        print("\n" + "="*60)
        print("📈 全天营养摄入:")
        print("-"*60)
        
        print(f"🔥 总热量: {daily_total['calories']:.0f}千卡")
        calories_pct = (daily_total['calories'] / self.daily_reference['calories']) * 100
        print(f"   📊 达到推荐量的{calories_pct:.1f}%")
        
        print(f"🥚 蛋白质: {daily_total['protein']:.1f}g")
        protein_pct = (daily_total['protein'] / self.daily_reference['protein']) * 100
        print(f"   📊 达到推荐量的{protein_pct:.1f}%")
        
        print(f"🥑 脂肪: {daily_total['fat']:.1f}g")
        fat_min = self.daily_reference['fat']['min']
        fat_max = self.daily_reference['fat']['max']
        if daily_total['fat'] < fat_min:
            print(f"   ⚠️  脂肪摄入偏低（建议>{fat_min:.1f}g）")
        elif daily_total['fat'] > fat_max:
            print(f"   ⚠️  脂肪摄入偏高（建议<{fat_max:.1f}g）")
        else:
            print(f"   ✅ 脂肪摄入合理")
        
        # 热量来源分析
        print("\n📊 热量来源比例:")
        protein_kcal = daily_total['protein'] * 4
        fat_kcal = daily_total['fat'] * 9
        carbs_kcal = daily_total['carbs'] * 4
        
        if daily_total['calories'] > 0:
            protein_pct_kcal = (protein_kcal / daily_total['calories']) * 100
            fat_pct_kcal = (fat_kcal / daily_total['calories']) * 100
            carbs_pct_kcal = (carbs_kcal / daily_total['calories']) * 100
            
            print(f"   蛋白质: {protein_pct_kcal:.1f}% （推荐: 10-15%）")
            print(f"   脂肪: {fat_pct_kcal:.1f}% （推荐: 20-30%）")
            print(f"   碳水: {carbs_pct_kcal:.1f}% （推荐: 50-65%）")
        
        # 其他营养素
        print("\n💊 其他营养素:")
        print(f"   膳食纤维: {daily_total['fiber']:.1f}g （推荐: {self.daily_reference['fiber']}g）")
        print(f"   钙: {daily_total['calcium']:.0f}mg （推荐: {self.daily_reference['calcium']}mg）")
        print(f"   铁: {daily_total['iron']:.1f}mg （推荐: {self.daily_reference['iron']}mg）")
        print(f"   维生素C: {daily_total['vitamin_c']:.0f}mg （推荐: {self.daily_reference['vitamin_c']}mg）")
        
        # 健康评分
        score = self.calculate_health_score(daily_total)
        print(f"\n⭐ 健康评分: {score}/100")
        
        # 建议
        self.give_recommendations(daily_total)
        
        # 保存报告
        self.save_report(daily_total, meals, score)
        
        return daily_total
    
    def calculate_health_score(self, nutrients):
        """计算饮食健康评分"""
        score = 100
        
        # 热量评分
        calories_ratio = nutrients['calories'] / self.daily_reference['calories']
        if calories_ratio < 0.8 or calories_ratio > 1.2:
            score -= 20
        
        # 蛋白质评分
        protein_ratio = nutrients['protein'] / self.daily_reference['protein']
        if protein_ratio < 0.8:
            score -= 15
        
        # 脂肪评分
        fat_kcal = nutrients['fat'] * 9
        fat_pct = (fat_kcal / nutrients['calories']) * 100 if nutrients['calories'] > 0 else 0
        if fat_pct < 20 or fat_pct > 30:
            score -= 15
        
        # 纤维评分
        if nutrients['fiber'] < self.daily_reference['fiber'] * 0.8:
            score -= 10
        
        return max(0, score)
    
    def give_recommendations(self, nutrients):
        """给出饮食建议"""
        print("\n💡 饮食建议:")
        
        # 热量建议
        calories_ratio = nutrients['calories'] / self.daily_reference['calories']
        if calories_ratio < 0.8:
            print("   🔼 热量摄入不足，建议增加主食和蛋白质摄入")
        elif calories_ratio > 1.2:
            print("   🔽 热量摄入过高，建议减少高热量食物")
        
        # 蛋白质建议
        if nutrients['protein'] < self.daily_reference['protein'] * 0.8:
            print("   🔼 蛋白质摄入不足，建议增加蛋、奶、豆制品")
        
        # 纤维建议
        if nutrients['fiber'] < self.daily_reference['fiber']:
            print("   🔼 膳食纤维不足，建议增加蔬菜、水果、全谷物")
    
    def save_report(self, nutrients, meals, score):
        """保存分析报告"""
        try:
            filename = f"diet_report_{datetime.now().strftime('%Y%m%d')}.txt"
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write("="*60 + "\n")
                f.write("📊 饮食分析报告\n")
                f.write("="*60 + "\n\n")
                f.write(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
                
                f.write("🍽️ 三餐记录:\n")
                for meal_type, meal_items in meals.items():
                    f.write(f"\n{meal_type}:\n")
                    for item in meal_items:
                        f.write(f"  • {item.get('name')}: {item.get('grams')}g\n")
                
                f.write("\n" + "="*60 + "\n")
                f.write("📈 营养分析:\n")
                f.write("-"*60 + "\n")
                
                f.write(f"总热量: {nutrients['calories']:.0f}千卡\n")
                f.write(f"蛋白质: {nutrients['protein']:.1f}g\n")
                f.write(f"脂肪: {nutrients['fat']:.1f}g\n")
                f.write(f"碳水: {nutrients['carbs']:.1f}g\n")
                f.write(f"膳食纤维: {nutrients['fiber']:.1f}g\n")
                f.write(f"钙: {nutrients['calcium']:.0f}mg\n")
                f.write(f"铁: {nutrients['iron']:.1f}mg\n")
                f.write(f"维生素C: {nutrients['vitamin_c']:.0f}mg\n\n")
                
                f.write(f"健康评分: {score}/100\n")
                
                f.write("\n💡 建议:\n")
                # 这里可以添加具体的建议内容
                f.write("保持均衡饮食，多吃蔬菜水果，适量摄入蛋白质\n")
                
                f.write("="*60 + "\n")
            
            print(f"💾 报告已保存到: {filename}")
        except Exception as e:
            print(f"💾 保存失败: {e}")

def main():
    analyzer = DietAnalyzer()
    
    # 示例数据：一日三餐
    sample_meals = {
        "早餐": [
            {"name": "牛奶", "grams": 250},
            {"name": "鸡蛋", "grams": 50},
            {"name": "面包", "grams": 100},
        ],
        "午餐": [
            {"name": "米饭", "grams": 200},
            {"name": "鸡胸肉", "grams": 150},
            {"name": "番茄", "grams": 100},
            {"name": "菠菜", "grams": 100},
        ],
        "晚餐": [
            {"name": "米饭", "grams": 150},
            {"name": "鸡蛋", "grams": 100},
            {"name": "白菜", "grams": 200},
        ]
    }
    
    print("示例饮食分析:")
    analyzer.analyze_day(sample_meals)

if __name__ == "__main__":
    main()