import pygame
import random
from collections import deque

# Initialize
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800
FPS = 60
SLIDE_SPEED = 25

# Palette
C_BG = (10, 8, 20)
C_WALL = (30, 35, 70)
C_WALL_EDGE = (0, 255, 200)
C_MASK = (255, 240, 0)
C_STAR = (255, 50, 255)
C_SPIKE = (255, 40, 40)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
raw_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
f_l = pygame.font.SysFont("monospace", 60, bold=True)
f_s = pygame.font.SysFont("monospace", 24, bold=True)
f_xs = pygame.font.SysFont("monospace", 18, bold=True)

def create_spritesheet():
    sheet = pygame.Surface((200, 40), pygame.SRCALPHA)
    pygame.draw.rect(sheet, C_MASK, (4, 4, 32, 32), border_radius=4)
    pygame.draw.rect(sheet, (0,0,0), (10, 10, 6, 10))
    pygame.draw.rect(sheet, (0,0,0), (24, 10, 6, 10))
    pygame.draw.polygon(sheet, C_SPIKE, [(50, 36), (60, 6), (70, 36)])
    pygame.draw.circle(sheet, C_STAR, (100, 20), 14, 4)
    pygame.draw.circle(sheet, (255, 255, 255), (100, 20), 5)
    return sheet

SPRITES = create_spritesheet()

# --- MOVEMENT & SOLVER ---

def get_stop_point(grid, x, y, dx, dy, w, h):
    cx, cy = x, y
    while True:
        nx, ny = cx + dx, cy + dy
        if 0 <= nx < w and 0 <= ny < h and grid[ny][nx] == 0:
            cx, cy = nx, ny
        else:
            return cx, cy

def is_solvable(grid, start, stars, goal, spikes, w, h):
    star_targets = [tuple(s) for s in stars]
    target_mask = (1 << len(stars)) - 1
    queue = deque([(start[0], start[1], 0)])
    visited = {(start[0], start[1], 0)}
    limit = 0
    while queue:
        cx, cy, mask = queue.popleft()
        limit += 1
        if limit > 3000: return False 
        if (cx, cy) == tuple(goal) and mask == target_mask: return True
        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            tx, ty, new_mask, hit_spike = cx, cy, mask, False
            while True:
                nx, ny = tx + dx, ty + dy
                if 0 <= nx < w and 0 <= ny < h and grid[ny][nx] == 0:
                    tx, ty = nx, ny
                    if (tx, ty) in spikes: hit_spike = True; break
                    if (tx, ty) in star_targets: new_mask |= (1 << star_targets.index((tx, ty)))
                else: break
            if not hit_spike and (tx, ty, new_mask) not in visited:
                visited.add((tx, ty, new_mask)); queue.append((tx, ty, new_mask))
    return False

# --- DUAL ALGORITHM GENERATOR ---
def generate_level(diff):
    sizes = {"Easy": (12, 10), "Medium": (20, 15), "Hard": (40, 30)}
    # Increased star counts for Hard
    counts = {"Easy": 3, "Medium": 5, "Hard": 12}
    W, H = sizes[diff]
    
    while True:
        pygame.event.pump()
        grid = [[1 for _ in range(W)] for _ in range(H)]
        
        if diff == "Hard":
            # Backbone Algorithm for Speed + High Star count
            curr_x, curr_y = random.randint(2, W-3), random.randint(2, H-3)
            ps, nodes = [curr_x, curr_y], []
            for _ in range(counts[diff] + 1):
                tx, ty = random.randint(1, W-2), random.randint(1, H-2)
                for x in range(min(curr_x, tx), max(curr_x, tx) + 1): grid[curr_y][x] = 0
                curr_x = tx
                for y in range(min(curr_y, ty), max(curr_y, ty) + 1): grid[y][curr_x] = 0
                curr_y = ty
                nodes.append([curr_x, curr_y])
            gl, stars = nodes.pop(), nodes[:counts[diff]]
            # Add noise for visual complexity
            for _ in range(int(W*H*0.1)): grid[random.randint(1, H-2)][random.randint(1, W-2)] = 0
        else:
            # Original Random Walk for Easy/Medium (Balanced)
            cx, cy = W//2, H//2
            for _ in range(W*H*2):
                grid[cy][cx] = 0
                d = random.choice([(0,1), (0,-1), (1,0), (-1,0)])
                cx, cy = max(1, min(W-2, cx+d[0])), max(1, min(H-2, cy+d[1]))
            ps, gl = [random.randint(1, W-2), random.randint(1, H-2)], [random.randint(1, W-2), random.randint(1, H-2)]
            if grid[ps[1]][ps[0]] != 0 or grid[gl[1]][gl[0]] != 0 or ps == gl: continue
            pot = [[c, r] for r in range(1, H-1) for c in range(1, W-1) if grid[r][c] == 0 and [c,r] not in [ps, gl]]
            if len(pot) < counts[diff]: continue
            stars = random.sample(pot, counts[diff])

        # Spike Density boost for Hard
        spikes = []
        spike_chance = 0.08 if diff == "Hard" else 0.08
        for _ in range(int(W*H*spike_chance)):
            sp = (random.randint(1, W-2), random.randint(1, H-2))
            if grid[sp[1]][sp[0]] == 0 and list(sp) not in stars + [ps, gl]: spikes.append(sp)
        
        if is_solvable(grid, ps, stars, gl, spikes, W, H): return grid, ps, gl, spikes, stars, W, H

class Button:
    def __init__(self, x, y, w, h, text, color, font_size="S"):
        self.rect = pygame.Rect(x, y, w, h)
        self.text, self.color, self.hover = text, color, False
        self.font = f_s if font_size == "S" else f_xs
    def draw(self, surf):
        c = tuple(min(255, v + 40) for v in self.color) if self.hover else self.color
        pygame.draw.rect(surf, c, self.rect, border_radius=8)
        pygame.draw.rect(surf, C_WALL_EDGE, self.rect, 2, border_radius=8)
        t = self.font.render(self.text, True, (255,255,255))
        surf.blit(t, (self.rect.centerx-t.get_width()//2, self.rect.centery-t.get_height()//2))

class NeonApp:
    def __init__(self):
        self.state = "MENU"
        self.btns = [Button(350, 300, 300, 60, "EASY", (30, 80, 30)),
                     Button(350, 400, 300, 60, "MEDIUM", (80, 80, 30)),
                     Button(350, 500, 300, 60, "HARD", (80, 30, 30))]
        self.reset_btn = Button(880, 740, 100, 40, "RESET", (100, 40, 40), "XS")
        self.diff, self.shake = "Easy", 0

    def start_level(self, diff, same=False):
        if not same:
            screen.fill(C_BG); txt = f_s.render(f"SYNCING {diff.upper()} SECTOR...", True, C_WALL_EDGE)
            screen.blit(txt, (500-txt.get_width()//2, 400)); pygame.display.flip()
            self.lvl_data = generate_level(diff)
        g, ps, gl, sp, st, w, h = self.lvl_data
        self.grid, self.p_grid, self.goal, self.spikes, self.stars = g, list(ps), gl, list(sp), list(st)
        self.w, self.h = w, h
        self.ts = 40 if diff == "Easy" else 30 if diff == "Medium" else 20
        self.off_x, self.off_y = (SCREEN_WIDTH-w*self.ts)//2, (SCREEN_HEIGHT-h*self.ts)//2
        self.pos = pygame.Vector2(ps[0]*self.ts + self.off_x, ps[1]*self.ts + self.off_y)
        self.target, self.moving, self.collected, self.total, self.state, self.diff = pygame.Vector2(self.pos), False, 0, len(st), "PLAY", diff

    def update(self):
        if self.shake > 0: self.shake *= 0.8
        if self.state == "PLAY" and self.moving:
            old_pos = pygame.Vector2(self.pos)
            vec = self.target - self.pos
            if vec.length() < SLIDE_SPEED:
                self.pos, self.moving = pygame.Vector2(self.target), False
            else:
                self.pos += vec.normalize() * SLIDE_SPEED
            
            # Sub-tile collision for star collection
            steps = int(vec.length() / 10) + 1
            for i in range(steps + 1):
                inter_pos = old_pos + (self.pos - old_pos) * (i / steps)
                gx, gy = int((inter_pos.x-self.off_x+self.ts//2)//self.ts), int((inter_pos.y-self.off_y+self.ts//2)//self.ts)
                if (gx, gy) in self.spikes: self.state, self.shake = "DEAD", 20
                for s in self.stars[:]:
                    if gx == s[0] and gy == s[1]: self.stars.remove(s); self.collected += 1; self.shake = 8
            
            if not self.moving:
                gx, gy = int((self.pos.x-self.off_x)//self.ts), int((self.pos.y-self.off_y)//self.ts)
                if gx == self.goal[0] and gy == self.goal[1] and self.collected == self.total: self.state, self.shake = "WIN", 12

    def draw(self):
        raw_surf.fill(C_BG); ox, oy = (random.uniform(-self.shake, self.shake), random.uniform(-self.shake, self.shake)) if self.shake > 1 else (0,0)
        if self.state == "MENU":
            t = f_l.render("NEON MASK", True, C_MASK); raw_surf.blit(t, (500-t.get_width()//2, 160))
            for b in self.btns: b.draw(raw_surf)
        else:
            for r in range(self.h):
                for c in range(self.w):
                    if self.grid[r][c] == 1:
                        pygame.draw.rect(raw_surf, C_WALL, (c*self.ts+self.off_x+ox, r*self.ts+self.off_y+oy, self.ts, self.ts))
                        pygame.draw.rect(raw_surf, C_WALL_EDGE, (c*self.ts+self.off_x+ox, r*self.ts+self.off_y+oy, self.ts, self.ts), 1)
            for s in self.spikes: raw_surf.blit(pygame.transform.scale(SPRITES.subsurface(40,0,40,40),(self.ts,self.ts)), (s[0]*self.ts+self.off_x+ox, s[1]*self.ts+self.off_y+oy))
            for s in self.stars: raw_surf.blit(pygame.transform.scale(SPRITES.subsurface(80,0,40,40),(self.ts,self.ts)), (s[0]*self.ts+self.off_x+ox, s[1]*self.ts+self.off_y+oy))
            g_c = C_MASK if self.collected == self.total else (50,50,50)
            pygame.draw.rect(raw_surf, g_c, (self.goal[0]*self.ts+self.off_x+ox+2, self.goal[1]*self.ts+self.off_y+oy+2, self.ts-4, self.ts-4), 2)
            if self.state != "DEAD": raw_surf.blit(pygame.transform.scale(SPRITES.subsurface(0,0,40,40),(self.ts,self.ts)), (self.pos.x+ox, self.pos.y+oy))
            if self.state in ["DEAD", "WIN"]:
                txt, col = ("CRASHED", C_SPIKE) if self.state == "DEAD" else ("CLEARED", C_WALL_EDGE)
                over = f_l.render(txt, True, col); raw_surf.blit(over, (500-over.get_width()//2, 350))
            self.reset_btn.draw(raw_surf)
        screen.blit(pygame.transform.smoothscale(raw_surf, (1020, 820)), (-10, -10)); pygame.display.flip()

app = NeonApp()
while True:
    m_pos = pygame.mouse.get_pos()
    for e in pygame.event.get():
        if e.type == pygame.QUIT: pygame.quit(); exit()
        if e.type == pygame.MOUSEBUTTONDOWN:
            if app.state == "MENU":
                for i, b in enumerate(app.btns):
                    if b.rect.collidepoint(m_pos): app.start_level(["Easy", "Medium", "Hard"][i])
            elif app.state != "MENU" and app.reset_btn.rect.collidepoint(m_pos): app.start_level(app.diff, same=True)
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE: app.state = "MENU"
            if e.key == pygame.K_r and app.state != "MENU": app.start_level(app.diff, same=True)
            if app.state == "PLAY" and not app.moving:
                keys = {pygame.K_UP:(0,-1), pygame.K_DOWN:(0,1), pygame.K_LEFT:(-1,0), pygame.K_RIGHT:(1,0)}
                if e.key in keys:
                    dx, dy = keys[e.key]
                    nx, ny = get_stop_point(app.grid, app.p_grid[0], app.p_grid[1], dx, dy, app.w, app.h)
                    if [nx, ny] != app.p_grid: app.target, app.p_grid, app.moving = pygame.Vector2(nx*app.ts+app.off_x, ny*app.ts+app.off_y), [nx, ny], True
            elif (app.state == "WIN" or app.state == "DEAD") and e.key == pygame.K_SPACE: app.start_level(app.diff, same=False)
    if app.state == "MENU":
        for b in app.btns: b.hover = b.rect.collidepoint(m_pos)
    else: app.reset_btn.hover = app.reset_btn.rect.collidepoint(m_pos)
    app.update(); app.draw(); clock.tick(FPS)
