# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw

class SelectionTool:
    def __init__(self):
        self.mode = 'RECT'
        self.points = []
        self.start = None
        self.end = None
        self.selecting = False
        self.figure_id = None
        self.active = False

    def start_selection(self, point, mode='RECT'):
        if point is None or point[0] is None:
            return

        self.mode = mode
        self.start = point
        self.end = point
        self.points = [point] if mode == 'LASSO' else []
        self.selecting = True
        self.active = False

    def update_selection(self, point, graph):
        if not self.selecting:
            return
        if point is None or point[0] is None:
            return

        if self.figure_id:
            try:
                graph.delete_figure(self.figure_id)
            except:
                pass

        if self.mode == 'LASSO':
            self.points.append(point)
            if len(self.points) > 1:
                self.figure_id = graph.draw_polygon(
                    self.points,
                    line_color='red', line_width=2, fill_color=None
                )
        else:
            self.end = point
            x1, y1 = self.start
            x2, y2 = self.end

            if self.mode == 'RECT':
                self.figure_id = graph.draw_rectangle(
                    (x1, y1), (x2, y2), line_color='red', line_width=2
                )
            elif self.mode == 'ELLIPSE':
                self.figure_id = graph.draw_oval(
                    (x1, y1), (x2, y2), line_color='red', line_width=2
                )

    def finish_selection(self, graph):
        if not self.selecting:
            return

        self.selecting = False

        if self.mode == 'LASSO':
            if len(self.points) > 2:
                self.active = True
        else:
            if self.start and self.end:
                self.active = True

    def clear_selection(self, graph):
        if self.figure_id:
            try:
                graph.delete_figure(self.figure_id)
            except:
                pass

        self.points = []
        self.start = None
        self.end = None
        self.selecting = False
        self.active = False
        self.figure_id = None

    def create_mask(self, image_size):
        if not self.active:
            return None

        mask = Image.new('L', image_size, 0)
        draw = ImageDraw.Draw(mask)

        if self.mode == 'RECT':
            if not self.start or not self.end:
                return None
            x1, y1 = self.start
            x2, y2 = self.end
            draw.rectangle([min(x1,x2), min(y1,y2), max(x1,x2), max(y1,y2)], fill=255)

        elif self.mode == 'ELLIPSE':
            x1, y1 = self.start
            x2, y2 = self.end
            draw.ellipse([min(x1,x2), min(y1,y2), max(x1,x2), max(y1,y2)], fill=255)

        elif self.mode == 'LASSO':
            if len(self.points) > 2:
                draw.polygon(self.points, fill=255)

        return mask

    def has_selection(self):
        return self.active
