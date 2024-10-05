import pygame as py
import os


def load_tile_surface(src, tile_size):
    src = src
    surf = py.image.load(src).convert_alpha()
    surf = py.transform.scale(surf, (tile_size, tile_size))

    return surf

class Tile:
    def __init__(self, tile_type:str, variant:int, data_pos:tuple|list, size:int|float, surf:py.Surface):
        self.tile_type = tile_type
        self.variant = variant
        self.size = size

        self.pos = data_pos

        self.image = surf

        self.rect = self.image.get_rect()
        # converting data position to world position
        self.rect.x = self.pos[0] * self.size
        self.rect.y = self.pos[1] * self.size

    def draw(self, draw_surf:py.Surface, camera_offset:tuple|list):
        draw_surf.blit(self.image, (self.rect.x + camera_offset[0], self.rect.y + camera_offset[1]))
    
    def change_tile(self, tile_type:str, variant:int, surf:py.Surface):
        self.tile_type = tile_type
        self.variant = variant
        self.image = surf

class TileMapManager:
    def __init__(self, window):
        self.display_window = window
        self.WIDTH, self.HEIGHT = self.display_window.get_width(), self.display_window.get_height()

        # auto tile settings
        self.tile_size = 32
        self.tile_types = ['stone']
        self.tile_variants = {}
        self.tile_maps = {
            # tile type: {
            # topleft: int(variant)
            # }
        }
        self.assets_path = {'stone': 'D:\Projects\Climb\data\\assets\\tiles\stone/'}

        # tile map settings
        self.AUTO_MAPPING_TYPES = {'stone'}
        self.MIXTURE_TYPES = {}

        self.ADJACENT_NEIGHBOR_MAP = {
            # tileset
            tuple(sorted([(0, 1), (1, 0)])): 'topleft', # topleft
            tuple(sorted([(0, 1), (1, 0), (-1, 0)])): 'top', # middletop
            tuple(sorted([(0, 1), (-1, 0)])): 'topright', # topright

            tuple(sorted([(0, -1), (1, 0), (0, 1)])): 'left', # left
            tuple(sorted([(0, 1), (1, 0), (0, -1), (-1, 0)])): 'middle', # middle
            tuple(sorted([(0, 1), (-1, 0), (0, -1)])): 'right', # right

            tuple(sorted([(0, -1), (1, 0)])): 'bottomleft', # bottomleft
            tuple(sorted([(0, -1), (-1, 0), (1, 0)])): 'bottom', # bottom
            tuple(sorted([(0, -1), (-1, 0)])): 'bottomright', # bottomright

            # vertical tiles
            tuple(sorted([(0, 1)])): 'vtop', # top
            tuple(sorted([(0, -1), (0, 1)])): 'vmiddle', # middle
            tuple(sorted([(0, -1)])): 'vbottom', # bottom

            # horizontal tiles
            tuple(sorted([(1, 0)])): 'hleft', # left
            tuple(sorted([(1, 0), (-1, 0)])): 'hmiddle', # middle
            tuple(sorted([(-1, 0)])): 'hright', # right

            # single tile
            tuple(sorted([])): 'single', # center
        }
        self.CORNER_NEIGHBOR_MAP = {
        tuple(sorted([(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (1, -1), (-1, 1)])): 9, # top left
        tuple(sorted([(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (1, -1), (1, 1)])): 10, # top right
        tuple(sorted([(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, 1)])): 11, # bottom left
        tuple(sorted([(0, 1), (1, 0), (0, -1), (-1, 0), (1, -1), (-1, 1), (1, 1)])): 12 # bottom right
        }

        self.adjacent_neighbor_offsets = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        self.corner_neighbor_offsets = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        self.tiles = {}
        self.current_tile_type = 0
        self.current_tile_variant = 0

        # chunk and grid
        self.chunk_size = [16, 9]
        self.world_chunk_size = [i*self.tile_size for i in self.chunk_size]
        
        # overlay grids
        self.grid_manager = GridManager(self.tile_size)
        self.grid_manager.generate_grid_chunk((100, 100))

        # self.holding_shift = False
        self.mode = 'brush'

        # load
        self.load_data(self.assets_path, self.tile_size)

    def load_data(self, assets_path, tile_size):
        for tile_type in assets_path:
            self.tile_types.append(tile_type) # add tile types
            self.tile_variants[tile_type] = {} # make empty dict for variants

            img_srcs = os.listdir(assets_path[tile_type])
            try:
                img_srcs = sorted(img_srcs, key=lambda x: int(x.split('.')[0])) # sorting srcs by name
            except TypeError:
                pass
            except ValueError:
                pass
            for i, img_src in enumerate(img_srcs):
                src = f"{assets_path[tile_type]}{img_src}"
                img = load_tile_surface(src, tile_size) # load image
                self.tile_variants[tile_type][i] = img # add image to variants

    def add(self, tile_pos):
        self.tiles[tile_pos] = Tile(self.tile_types[self.current_tile_type], self.current_tile_variant, tile_pos, self.tile_size, self.tile_variants[self.tile_types[self.current_tile_type]][self.current_tile_variant])

        self.auto_tile([
            
            # offsets
            (tile_pos[0], tile_pos[1]), # middle

            (tile_pos[0] + 1, tile_pos[1]), # right
            (tile_pos[0] - 1, tile_pos[1]), # left

            (tile_pos[0], tile_pos[1] + 1), # bottom
            (tile_pos[0], tile_pos[1] - 1), # top

            (tile_pos[0] + 1, tile_pos[1] + 1), # bottom right
            (tile_pos[0] - 1, tile_pos[1] + 1), # bottom left
            
            (tile_pos[0] + 1, tile_pos[1] - 1), # top right
            (tile_pos[0] - 1, tile_pos[1] - 1), # top left
        ])

    def delete(self, tile_pos):
        try:
            del self.tiles[tile_pos]

            self.auto_tile([
            
            # offsets
            (tile_pos[0], tile_pos[1]), # middle

            (tile_pos[0] + 1, tile_pos[1]), # right
            (tile_pos[0] - 1, tile_pos[1]), # left

            (tile_pos[0], tile_pos[1] + 1), # bottom
            (tile_pos[0], tile_pos[1] - 1), # top

            (tile_pos[0] + 1, tile_pos[1] + 1), # bottom right
            (tile_pos[0] - 1, tile_pos[1] + 1), # bottom left
            
            (tile_pos[0] + 1, tile_pos[1] - 1), # top right
            (tile_pos[0] - 1, tile_pos[1] - 1), # top left
        ])
            
        except KeyError:
            pass

    def change_variant(self, y):
        if y == 1:
            self.current_tile_variant = (self.current_tile_variant + 1) % len(self.tile_variants[self.tile_types[self.current_tile_type]].keys())
        elif y == -1:
            self.current_tile_variant = (self.current_tile_variant - 1) % len(self.tile_variants[self.tile_types[self.current_tile_type]].keys())

    def change_type(self, y):
        if y == 1:
            self.current_tile_type = (self.current_tile_type + 1) % len(self.tile_types)
        elif y == -1:
            self.current_tile_type = (self.current_tile_type - 1) % len(self.tile_types)

    def change_modes(self, key):
        if key == py.K_e:
            self.mode = 'eraser'
        elif key == py.K_b:
            self.mode = 'brush'

    def draw(self, draw_surf, camera_offset):
        [tile.draw(draw_surf, camera_offset) for tile in self.tiles.values()]

    def draw_tile_overlay(self, draw_surf, pos, camera_offset):
        draw_surf.blit(self.tile_variants[self.tile_types[self.current_tile_type]][self.current_tile_variant], (pos[0] * self.tile_size + camera_offset[0], pos[1] * self.tile_size + camera_offset[1]))

    def auto_tile(self, tiles_pos):
        for pos in tiles_pos:
            try:
                tile = self.tiles[pos]
                tile_type = tile.tile_type

                neighbor_offsets = set()

                # adjacent neighbor offsets
                for shift in self.adjacent_neighbor_offsets:
                    offset = pos[0] + shift[0], pos[1] + shift[1]

                    if offset in self.tiles:
                        if self.tiles[offset].tile_type in self.AUTO_MAPPING_TYPES:
                            if self.tiles[offset].tile_type in self.MIXTURE_TYPES: # Mixture Tiles
                                neighbor_offsets.add(shift)
                            elif self.tiles[offset].tile_type == tile_type: # Non Mixture Tiles
                                neighbor_offsets.add(shift)

                self.tiles[pos].change_tile(tile_type, self.ADJACENT_NEIGHBOR_MAP[tuple(sorted(neighbor_offsets))], self.tile_variants[tile_type][self.ADJACENT_NEIGHBOR_MAP[tuple(sorted(neighbor_offsets))]])
        
                # corner neighbor offsets
                neighbor_offsets = set(neighbor_offsets)
                for shift in self.corner_neighbor_offsets:
                    offset = pos[0] + shift[0], pos[1] + shift[1]

                    if offset in self.tiles:
                        if self.tiles[offset].tile_type in self.AUTO_MAPPING_TYPES:
                            if self.tiles[offset].tile_type in self.MIXTURE_TYPES: # Mixture Tiles
                                neighbor_offsets.add(shift)
                            elif self.tiles[offset].tile_type == tile_type: # Non Mixture Tiles
                                neighbor_offsets.add(shift)
                
                self.tiles[pos].change_tile(tile_type, self.CORNER_NEIGHBOR_MAP[tuple(sorted(neighbor_offsets))], self.tile_variants[tile_type][self.CORNER_NEIGHBOR_MAP[tuple(sorted(neighbor_offsets))]])
                
            except KeyError:
                pass

    def mouse_wheel(self, y):
        if py.key.get_pressed()[py.K_LSHIFT]:
            self.change_type(y)
        else:
            self.change_variant(y)
        
    def keyboard_down(self, key):
        self.change_modes(key)

    def button_control(self, buttons):
        if buttons[0]:
            match self.mode:
                case 'brush':
                    self.add(self.tile_grid_pos)
                case 'eraser':
                    self.delete(self.tile_grid_pos)

    def update(self, pos, camera_offset):
        # position
        self.real_world_pos = pos[0] - camera_offset[0], pos[1] - camera_offset[1]
        self.tile_grid_pos = self.real_world_pos[0] // self.tile_size, self.real_world_pos[1] // self.tile_size

        self.grid_manager.update((self.WIDTH, self.HEIGHT), camera_offset)

        self.grid_manager.draw_bg(self.display_window, camera_offset)
        self.draw(self.display_window, camera_offset)
        self.draw_tile_overlay(self.display_window, self.tile_grid_pos, camera_offset)
        self.grid_manager.draw_grids(self.display_window, camera_offset)


class GridManager:
    def __init__(self, tile_size):
        self.grids = {}
        self.background_chunks = {}
        self.chunk_size = [12, 12]
        self.grid_size = [16*tile_size, 16*tile_size]
        self.tile_size = tile_size

        self.grid_chunk_pos = (0, 0)
    
    def generate_grid_chunk(self, pos):
        chunk_pos = pos
        # chunk_pos = tuple(get_floored_offset(pos, [self.grid_chunk_size[0]*self.tile_size, self.grid_chunk_size[1]*self.tile_size]))

        self.grids[chunk_pos] = [py.Surface((self.chunk_size[0]*self.grid_size[0], self.chunk_size[1]*self.grid_size[1]), py.SRCALPHA), [chunk_pos[0]*self.chunk_size[0]*self.grid_size[0], chunk_pos[1]*self.chunk_size[1]*self.grid_size[1]]]
        self.grids[chunk_pos][0].set_alpha(64)

        for x in range(self.chunk_size[0]):
            for y in range(self.chunk_size[1]):
                py.draw.rect(self.grids[chunk_pos][0], (0, 0, 255), (x*self.grid_size[0], y*self.grid_size[1], self.grid_size[0], self.grid_size[1]), 1)
       
        self.grids[chunk_pos][0].convert_alpha()
    
    def generate_transparent_bg(self, pos):
        chunk_pos = pos

        self.background_chunks[chunk_pos] = [py.Surface((self.chunk_size[0]*self.tile_size, self.chunk_size[1]*self.tile_size), py.SRCALPHA), [chunk_pos[0]*self.chunk_size[0]*self.tile_size, chunk_pos[1]*self.chunk_size[1]*self.tile_size]]
        self.background_chunks[chunk_pos][0].fill((100, 100, 100)) if (pos[0]+pos[1]) % 2 == 0 else self.background_chunks[chunk_pos][0].fill((241, 241, 241))
        self.background_chunks[chunk_pos][0].set_alpha(128 )
        self.background_chunks[chunk_pos][0].convert_alpha()


    def draw_grids(self, draw_surf, camera_offset):
        for shift in [
            # (-1, -2), (0, -2), (1, -2),
            (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1),
            (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0),
            (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1)
            # (-1, 2), (0, 2), (1, 2),
            ]:
            # shift = [0, 0]
            new_chunk_pos = self.grid_chunk_pos[0] + shift[0], self.grid_chunk_pos[1] + shift[1]
            try:
                surf, pos = self.grids[new_chunk_pos]
            except:
                self.generate_grid_chunk(new_chunk_pos)
                surf, pos = self.grids[new_chunk_pos]
            draw_surf.blit(surf, (pos[0]+camera_offset[0], pos[1]+camera_offset[1]))

    def draw_bg(self, draw_surf, camera_offset):
        for shift in [
            # (-1, -2), (0, -2), (1, -2),
            (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1),
            (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0),
            (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1)
            # (-1, 2), (0, 2), (1, 2),
            ]:
            new_chunk_pos = self.bg_chunk_pos[0] + shift[0], self.bg_chunk_pos[1] + shift[1]
            try:
                surf, pos = self.background_chunks[new_chunk_pos]
            except:
                self.generate_transparent_bg(new_chunk_pos)
                surf, pos = self.background_chunks[new_chunk_pos]
            draw_surf.blit(surf, (pos[0]+camera_offset[0], pos[1]+camera_offset[1]))
    
    def update(self, draw_surf_size, camera_offset):
        self.grid_chunk_pos = tuple(get_floored_offset((-camera_offset[0]+draw_surf_size[0]/2, -camera_offset[1]+draw_surf_size[1]/2), [self.chunk_size[0]*self.grid_size[0], self.chunk_size[1]*self.grid_size[1]]))
        self.bg_chunk_pos = tuple(get_floored_offset((-camera_offset[0]+draw_surf_size[0]/2, -camera_offset[1]+draw_surf_size[1]/2), [self.chunk_size[0]*self.tile_size, self.chunk_size[1]*self.tile_size]))
        print(self.grid_chunk_pos, self.bg_chunk_pos)


def get_floored_offset(pos:tuple|list, size:tuple|list) -> list:
    return [pos[0] // size[0], pos[1] // size[1]]