#!python
"""
智能购物清单生成器
根据菜谱自动生成购物清单
"""

import json
from datetime import datetime

class ShoppingListGenerator:
    def __init__(self):
        # 常见食材的单位换算
        self.unit_conversion = {
            "个": 1,
            "克": 1,
            "千克": 1000,
            "斤": 500,
            "两": 50,
            "毫升": 1,
            "升": 1000,
            "汤匙": 15,    # 1汤匙 ≈ 15g/15ml
            "茶匙": 5,     # 1茶匙 ≈ 5g/5ml
        }
        
        # 保存的购物清单
        self.shopping_lists = {}
    
    def parse_ingredient(self, ingredient_str):
        """解析食材字符串，如：'鸡蛋 3个' -> ('鸡蛋', 150)"""
        try:
            # 移除空格和特殊字符
            ingredient_str = ingredient_str.strip()
            
            # 分离数字和单位
            import re
            match = re.match(r'([\u4e00-\u9fa5a-zA-Z]+)\s*(\d*\.?\d+)?\s*([\u4e00-\u9fa5a-zA-Z]+)?', ingredient_str)
            
            if match:
                name = match.group(1)  # 食材名
                quantity = float(match.group(2)) if match.group(2) else 1  # 数量
                unit = match.group(3) if match.group(3) else "个"  # 单位
                
                # 转换为克
                if unit in self.unit_conversion:
                    grams = quantity * self.unit_conversion[unit]
                else:
                    grams = quantity  # 默认按克处理
                
                return name, round(grams, 2)
            else:
                return ingredient_str, 1
        except:
            return ingredient_str, 1
    
    def generate_from_recipes(self, recipes):
        """根据多个菜谱生成购物清单"""
        shopping_list = {}
        
        print("\n🛒 智能购物清单生成器")
        print("="*50)
        
        for recipe_name, ingredients in recipes.items():
            print(f"\n📝 菜谱: {recipe_name}")
            print("  需要食材:")
            
            for ingredient in ingredients:
                name, grams = self.parse_ingredient(ingredient)
                
                if name in shopping_list:
                    shopping_list[name] += grams
                else:
                    shopping_list[name] = grams
                
                print(f"    • {ingredient}")
        
        print("\n" + "="*50)
        print("📋 总计需要购买:")
        
        # 按类别分组显示
        categories = {
            "蔬菜类": ["番茄", "黄瓜", "白菜", "土豆", "胡萝卜", "青菜", "菠菜"],
            "肉蛋类": ["鸡蛋", "鸡肉", "猪肉", "牛肉", "鱼", "虾"],
            "主食类": ["大米", "面条", "面粉", "面包"],
            "调料类": ["油", "盐", "糖", "酱油", "醋"],
            "其他": []
        }
        
        total_cost = 0
        category_totals = {}
        
        for category, items in categories.items():
            category_items = {}
            for item, grams in shopping_list.items():
                for pattern in items:
                    if pattern in item:
                        category_items[item] = grams
                        break
            
            if category_items:
                print(f"\n{category}:")
                for item, grams in category_items.items():
                    # 估算价格（粗略估算）
                    estimated_price = self.estimate_price(item, grams)
                    total_cost += estimated_price
                    
                    if category not in category_totals:
                        category_totals[category] = 0
                    category_totals[category] += estimated_price
                    
                    # 转换为常用单位显示
                    display_amount = self.convert_to_best_unit(grams, item)
                    print(f"  ✓ {item}: {display_amount} ≈ {estimated_price:.2f}元")
        
        print("\n" + "="*50)
        print(f"💰 预估总花费: {total_cost:.2f}元")
        
        # 显示分类花费
        print("\n📊 分类花费:")
        for category, cost in category_totals.items():
            percentage = (cost / total_cost * 100) if total_cost > 0 else 0
            print(f"  {category}: {cost:.2f}元 ({percentage:.1f}%)")
        
        # 保存购物清单
        self.save_shopping_list(shopping_list, total_cost, recipes)
        
        return shopping_list
    
    def estimate_price(self, item, grams):
        """估算食材价格（基于市场均价）"""
        price_per_kg = {
            "大米": 8,      # 8元/公斤
            "鸡蛋": 12,     # 12元/公斤
            "番茄": 6,      # 6元/公斤
            "黄瓜": 5,      # 5元/公斤
            "鸡肉": 20,     # 20元/公斤
            "猪肉": 30,     # 30元/公斤
            "牛肉": 80,     # 80元/公斤
            "油": 15,       # 15元/升
            "盐": 5,        # 5元/公斤
            "糖": 10,       # 10元/公斤
        }
        
        # 查找匹配的价格
        for key, price in price_per_kg.items():
            if key in item:
                return (grams / 1000) * price
        
        # 默认价格
        return (grams / 1000) * 20
    
    def convert_to_best_unit(self, grams, item):
        """转换为最合适的单位显示"""
        if grams >= 1000:
            return f"{grams/1000:.2f}千克"
        elif grams >= 500 and "斤" in item:
            return f"{grams/500:.2f}斤"
        elif grams >= 50 and "两" in item:
            return f"{grams/50:.2f}两"
        else:
            return f"{grams:.0f}克"
    
    def save_shopping_list(self, items, total_cost, recipes):
        """保存购物清单到文件"""
        try:
            filename = f"shopping_list_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write("="*50 + "\n")
                f.write("🛒 购物清单\n")
                f.write("="*50 + "\n\n")
                f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
                
                f.write("📝 菜谱:\n")
                for recipe in recipes.keys():
                    f.write(f"  • {recipe}\n")
                
                f.write("\n📋 需要购买:\n")
                for item, grams in items.items():
                    display_amount = self.convert_to_best_unit(grams, item)
                    f.write(f"  ✓ {item}: {display_amount}\n")
                
                f.write(f"\n💰 预估总花费: {total_cost:.2f}元\n")
                f.write("="*50 + "\n")
            
            print(f"💾 购物清单已保存到: {filename}")
            return filename
        except Exception as e:
            print(f"💾 保存失败: {e}")
            return None
    
    def interactive_mode(self):
        """交互式生成购物清单"""
        print("🎮 交互式购物清单生成")
        print("输入菜谱（每行一个食材，空行结束菜谱）")
        print("格式示例: 鸡蛋 3个, 番茄 2个, 油 10克")
        
        recipes = {}
        recipe_count = 1
        
        while True:
            recipe_name = input(f"\n请输入第{recipe_count}个菜谱名称（输入'完成'结束）: ").strip()
            
            if recipe_name.lower() in ['完成', 'done', 'q', 'quit']:
                break
            
            print(f"请输入 {recipe_name} 的食材（每行一个，空行结束）:")
            ingredients = []
            
            while True:
                ingredient = input("食材: ").strip()
                if ingredient == "":
                    break
                ingredients.append(ingredient)
            
            if ingredients:
                recipes[recipe_name] = ingredients
                recipe_count += 1
            else:
                print("⚠️  没有输入食材，菜谱未添加")
        
        if recipes:
            print("\n" + "="*50)
            print("开始生成购物清单...")
            self.generate_from_recipes(recipes)
        else:
            print("⚠️  没有输入任何菜谱")

def main():
    generator = ShoppingListGenerator()
    
    # 示例数据
    sample_recipes = {
        "番茄炒蛋": ["鸡蛋 3个", "番茄 2个", "油 15克", "盐 5克", "糖 3克"],
        "米饭": ["大米 200克", "水 400毫升"],
        "凉拌黄瓜": ["黄瓜 2根", "蒜 3瓣", "醋 10毫升", "香油 5毫升"]
    }
    
    print("示例购物清单:")
    generator.generate_from_recipes(sample_recipes)
    
    # 询问是否使用交互模式
    use_interactive = input("\n是否使用交互模式生成购物清单？(y/n): ").strip().lower()
    if use_interactive == 'y':
        generator.interactive_mode()

if __name__ == "__main__":
    main()