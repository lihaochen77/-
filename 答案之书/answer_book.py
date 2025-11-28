import pygame
import random
import sys

class AnswerBook:
    def __init__(self):
        # 初始化pygame
        pygame.init()
        
        # 设置窗口大小和标题
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("答案之书")
        
        # 设置时钟
        self.clock = pygame.time.Clock()
        
        # 定义颜色
        self.colors = {
            "background": (245, 240, 230),
            "book": (255, 255, 255),
            "book_border": (139, 69, 19),
            "text": (0, 0, 0),
            "highlight": (255, 215, 0),
            "shadow": (169, 169, 169)
        }
        
        # 初始化字体 - 使用系统支持中文的字体
        # 尝试使用微软雅黑，如果不存在则使用默认字体
        try:
            self.font = pygame.font.SysFont("Microsoft YaHei", 36)
            self.title_font = pygame.font.SysFont("Microsoft YaHei", 48)
            self.answer_font = pygame.font.SysFont("Microsoft YaHei", 32)
        except:
            # 如果微软雅黑不可用，尝试使用宋体
            try:
                self.font = pygame.font.SysFont("SimSun", 36)
                self.title_font = pygame.font.SysFont("SimSun", 48)
                self.answer_font = pygame.font.SysFont("SimSun", 32)
            except:
                # 如果都不可用，使用默认字体
                self.font = pygame.font.Font(None, 36)
                self.title_font = pygame.font.Font(None, 48)
                self.answer_font = pygame.font.Font(None, 32)
        
        # 答案列表
        self.answers = [
            "是的",
            "不是",
            "当然",
            "绝对不行",
            "有可能",
            "不太可能",
            "建议你这样做",
            "最好不要",
            "听从你的内心",
            "再考虑一下",
            "时机尚未成熟",
            "很快就会实现",
            "保持耐心",
            "放手去做吧",
            "谨慎行事",
            "这是个好主意",
            "或许还有更好的选择",
            "相信自己",
            "命运掌握在你手中",
            "一切都会好起来的",
            "答案就在你心中",
            "需要更多信息",
            "现在不是时候",
            "值得一试",
            "三思而后行",
            "跟随直觉",
            "会有好结果的",
            "可能会遇到挑战",
            "保持乐观",
            "做好准备"
        ]
        
        # 当前状态
        self.current_answer = ""
        self.show_answer = False
        self.animation_progress = 0
        self.animating = False
        self.animation_type = "fade"  # fade 或 scale
        
        # 主循环
        self.running = True
    
    def draw_book(self):
        """绘制书籍界面"""
        # 绘制背景
        self.screen.fill(self.colors["background"])
        
        # 绘制书籍阴影
        shadow_rect = pygame.Rect(110, 60, 600, 500)
        pygame.draw.rect(self.screen, self.colors["shadow"], shadow_rect, border_radius=10)
        
        # 绘制书籍主体
        book_rect = pygame.Rect(100, 50, 600, 500)
        pygame.draw.rect(self.screen, self.colors["book"], book_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.colors["book_border"], book_rect, 5, border_radius=10)
        
        # 添加书籍纹理
        for i in range(0, 600, 20):
            pygame.draw.line(self.screen, (240, 240, 240), 
                           (100, 50 + i), (700, 50 + i), 1)
        
        # 绘制书籍标题
        title_text = self.title_font.render("答案之书", True, self.colors["book_border"])
        title_rect = title_text.get_rect(center=(self.width // 2, 120))
        # 添加标题阴影
        shadow_title = self.title_font.render("答案之书", True, self.colors["shadow"])
        self.screen.blit(shadow_title, (title_rect.x + 2, title_rect.y + 2))
        self.screen.blit(title_text, title_rect)
        
        # 绘制装饰线
        pygame.draw.line(self.screen, self.colors["book_border"], 
                       (150, 150), (650, 150), 2)
        pygame.draw.line(self.screen, self.colors["book_border"], 
                       (150, 450), (650, 450), 2)
        
        # 绘制提示文字
        hint_text = self.font.render("请在心中默念你的问题", True, self.colors["text"])
        hint_rect = hint_text.get_rect(center=(self.width // 2, 180))
        self.screen.blit(hint_text, hint_rect)
        
        # 绘制答案区域
        answer_area = pygame.Rect(150, 220, 500, 200)
        # 绘制答案区域背景渐变
        for i in range(200):
            alpha = int(255 * (i / 200))
            pygame.draw.line(self.screen, (255, 255, 255 - alpha // 10), 
                           (150, 220 + i), (650, 220 + i), 1)
        pygame.draw.rect(self.screen, self.colors["book_border"], answer_area, 3, border_radius=10)
        
        # 如果显示答案，绘制答案
        if self.show_answer:
            # 计算动画进度
            progress = self.animation_progress if self.animating else 1
            
            # 添加答案背景高光（带动画）
            highlight_rect = pygame.Rect(160, 230, 480, 180)
            if self.animation_type == "scale":
                # 缩放动画
                scale = 0.5 + 0.5 * progress
                scaled_width = int(480 * scale)
                scaled_height = int(180 * scale)
                scaled_rect = pygame.Rect(
                    160 + (480 - scaled_width) // 2,
                    230 + (180 - scaled_height) // 2,
                    scaled_width,
                    scaled_height
                )
                pygame.draw.rect(self.screen, (255, 255, 240), scaled_rect, border_radius=8)
            else:
                # 淡入动画
                highlight_surface = pygame.Surface((480, 180), pygame.SRCALPHA)
                alpha = int(255 * progress)
                highlight_surface.fill((255, 255, 240, alpha))
                self.screen.blit(highlight_surface, (160, 230))
            
            # 绘制答案文字（带动画）
            answer_text = self.answer_font.render(self.current_answer, True, self.colors["book_border"])
            answer_rect = answer_text.get_rect(center=(self.width // 2, 320))
            
            if self.animation_type == "scale":
                # 缩放动画
                scale = 0.5 + 0.5 * progress
                scaled_text = pygame.transform.scale(answer_text, 
                                                   (int(answer_text.get_width() * scale), 
                                                    int(answer_text.get_height() * scale)))
                scaled_rect = scaled_text.get_rect(center=(self.width // 2, 320))
            else:
                # 淡入动画
                text_surface = pygame.Surface(answer_text.get_size(), pygame.SRCALPHA)
                alpha = int(255 * progress)
                text_surface.fill((0, 0, 0, alpha), special_flags=pygame.BLEND_RGBA_MULT)
                text_surface.blit(answer_text, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
                scaled_text = text_surface
                scaled_rect = answer_rect
            
            # 添加答案阴影
            shadow_answer = self.answer_font.render(self.current_answer, True, self.colors["shadow"])
            if self.animation_type == "scale":
                scaled_shadow = pygame.transform.scale(shadow_answer, 
                                                    (int(shadow_answer.get_width() * scale), 
                                                     int(shadow_answer.get_height() * scale)))
                self.screen.blit(scaled_shadow, (scaled_rect.x + 2, scaled_rect.y + 2))
            else:
                shadow_surface = pygame.Surface(shadow_answer.get_size(), pygame.SRCALPHA)
                shadow_surface.fill((0, 0, 0, alpha), special_flags=pygame.BLEND_RGBA_MULT)
                shadow_surface.blit(shadow_answer, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
                self.screen.blit(shadow_surface, (answer_rect.x + 2, answer_rect.y + 2))
            
            self.screen.blit(scaled_text, scaled_rect)
            
            # 添加装饰性引号（带动画）
            quote_font = pygame.font.Font(None, 64)
            left_quote = quote_font.render("\"", True, (200, 200, 200))
            right_quote = quote_font.render("\"", True, (200, 200, 200))
            
            if self.animation_type == "scale":
                scaled_left = pygame.transform.scale(left_quote, 
                                                   (int(left_quote.get_width() * scale), 
                                                    int(left_quote.get_height() * scale)))
                scaled_right = pygame.transform.scale(right_quote, 
                                                    (int(right_quote.get_width() * scale), 
                                                     int(right_quote.get_height() * scale)))
            else:
                left_surface = pygame.Surface(left_quote.get_size(), pygame.SRCALPHA)
                left_surface.fill((0, 0, 0, alpha), special_flags=pygame.BLEND_RGBA_MULT)
                left_surface.blit(left_quote, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
                scaled_left = left_surface
                
                right_surface = pygame.Surface(right_quote.get_size(), pygame.SRCALPHA)
                right_surface.fill((0, 0, 0, alpha), special_flags=pygame.BLEND_RGBA_MULT)
                right_surface.blit(right_quote, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
                scaled_right = right_surface
            
            self.screen.blit(scaled_left, (200, 250))
            self.screen.blit(scaled_right, (550, 350))
        
        # 绘制交互提示
        interaction_text = self.font.render("点击屏幕或按空格键获取答案", True, self.colors["text"])
        interaction_rect = interaction_text.get_rect(center=(self.width // 2, 480))
        self.screen.blit(interaction_text, interaction_rect)
    
    def get_random_answer(self):
        """获取随机答案"""
        self.current_answer = random.choice(self.answers)
        self.show_answer = True
        self.animating = True
        self.animation_progress = 0
        # 随机选择动画类型
        self.animation_type = random.choice(["fade", "scale"])
    
    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 点击屏幕获取答案
                self.get_random_answer()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # 按空格键获取答案
                    self.get_random_answer()
                elif event.key == pygame.K_ESCAPE:
                    # 按ESC键退出
                    self.running = False
    
    def update(self):
        """更新游戏状态"""
        if self.animating:
            self.animation_progress += 0.05
            if self.animation_progress >= 1:
                self.animation_progress = 1
                self.animating = False
    
    def run(self):
        """主运行循环"""
        while self.running:
            # 处理事件
            self.handle_events()
            
            # 更新状态
            self.update()
            
            # 绘制界面
            self.draw_book()
            
            # 更新显示
            pygame.display.flip()
            
            # 控制帧率
            self.clock.tick(30)
        
        # 退出游戏
        pygame.quit()
        sys.exit()

# 运行游戏
if __name__ == "__main__":
    answer_book = AnswerBook()
    answer_book.run()