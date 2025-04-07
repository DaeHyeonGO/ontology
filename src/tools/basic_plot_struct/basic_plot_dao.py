from typing import List, Dict, Optional
from base_dao import BaseDAO

class BasicPlotDAO(BaseDAO):
    def create(self, sequence: int, title: str, theme: str, setting: str, main_conflict: str, 
               time_period: str = None, resolution: str = None) -> int:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO BasicPlot (sequence, title, theme, setting, time_period, main_conflict, resolution)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (sequence, title, theme, setting, time_period, main_conflict, resolution))
                connection.commit()
                return cursor.lastrowid
        except Exception as e:
            connection.rollback()
            raise e
    
    def get_by_id(self, plot_id: int) -> Optional[Dict]:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM BasicPlot WHERE id = %s"
                cursor.execute(sql, (plot_id,))
                return cursor.fetchone()
        except Exception as e:
            raise e
    
    def get_all(self) -> List[Dict]:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM BasicPlot"
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            raise e
    
    def update(self, plot_id: int, title: str = None, theme: str = None, setting: str = None,
               time_period: str = None, main_conflict: str = None, resolution: str = None) -> bool:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                updates = []
                params = []
                
                if title is not None:
                    updates.append("title = %s")
                    params.append(title)
                if theme is not None:
                    updates.append("theme = %s")
                    params.append(theme)
                if setting is not None:
                    updates.append("setting = %s")
                    params.append(setting)
                if time_period is not None:
                    updates.append("time_period = %s")
                    params.append(time_period)
                if main_conflict is not None:
                    updates.append("main_conflict = %s")
                    params.append(main_conflict)
                if resolution is not None:
                    updates.append("resolution = %s")
                    params.append(resolution)
                
                if not updates:
                    return False
                
                sql = f"UPDATE BasicPlot SET {', '.join(updates)} WHERE id = %s"
                params.append(plot_id)
                
                cursor.execute(sql, params)
                connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            connection.rollback()
            raise e
    
    def delete(self, plot_id: int) -> bool:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM BasicPlot WHERE id = %s"
                cursor.execute(sql, (plot_id,))
                connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            connection.rollback()
            raise e
    
    def add_genre(self, plot_id: int, genre: str) -> bool:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO BasicPlot_Genre (plot_id, genre)
                VALUES (%s, %s)
                """
                cursor.execute(sql, (plot_id, genre))
                connection.commit()
                return True
        except Exception as e:
            connection.rollback()
            raise e
    
    def remove_genre(self, plot_id: int, genre: str) -> bool:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                DELETE FROM BasicPlot_Genre 
                WHERE plot_id = %s AND genre = %s
                """
                cursor.execute(sql, (plot_id, genre))
                connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            connection.rollback()
            raise e
    
    def get_genres(self, plot_id: int) -> List[str]:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT genre FROM BasicPlot_Genre
                WHERE plot_id = %s
                """
                cursor.execute(sql, (plot_id,))
                results = cursor.fetchall()
                return [result['genre'] for result in results]
        except Exception as e:
            raise e
    
    def add_character(self, plot_id: int, character_id: int) -> bool:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO BasicPlot_Character (plot_id, character_id)
                VALUES (%s, %s)
                """
                cursor.execute(sql, (plot_id, character_id))
                connection.commit()
                return True
        except Exception as e:
            connection.rollback()
            raise e
    
    def remove_character(self, plot_id: int, character_id: int) -> bool:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                DELETE FROM BasicPlot_Character 
                WHERE plot_id = %s AND character_id = %s
                """
                cursor.execute(sql, (plot_id, character_id))
                connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            connection.rollback()
            raise e
    
    def get_characters(self, plot_id: int) -> List[Dict]:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT c.* FROM `Character` c
                JOIN BasicPlot_Character bpc ON c.id = bpc.character_id
                WHERE bpc.plot_id = %s
                """
                cursor.execute(sql, (plot_id,))
                return cursor.fetchall()
        except Exception as e:
            raise e
    
    def add_plotpoint(self, plot_id: int, plotpoint_id: int) -> bool:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO BasicPlot_PlotPoint (plot_id, plotpoint_id)
                VALUES (%s, %s)
                """
                cursor.execute(sql, (plot_id, plotpoint_id))
                connection.commit()
                return True
        except Exception as e:
            connection.rollback()
            raise e
    
    def remove_plotpoint(self, plot_id: int, plotpoint_id: int) -> bool:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                DELETE FROM BasicPlot_PlotPoint 
                WHERE plot_id = %s AND plotpoint_id = %s
                """
                cursor.execute(sql, (plot_id, plotpoint_id))
                connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            connection.rollback()
            raise e
    
    def get_plotpoints(self, plot_id: int) -> List[Dict]:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT pp.* FROM PlotPoint pp
                JOIN BasicPlot_PlotPoint bpp ON pp.id = bpp.plotpoint_id
                WHERE bpp.plot_id = %s
                """
                cursor.execute(sql, (plot_id,))
                return cursor.fetchall()
        except Exception as e:
            raise e
    
    def add_subplot_thread(self, plot_id: int, subplot_thread: str) -> bool:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO BasicPlot_SubplotThread (plot_id, subplot_thread)
                VALUES (%s, %s)
                """
                cursor.execute(sql, (plot_id, subplot_thread))
                connection.commit()
                return True
        except Exception as e:
            connection.rollback()
            raise e
    
    def remove_subplot_thread(self, plot_id: int, subplot_thread: str) -> bool:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                DELETE FROM BasicPlot_SubplotThread 
                WHERE plot_id = %s AND subplot_thread = %s
                """
                cursor.execute(sql, (plot_id, subplot_thread))
                connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            connection.rollback()
            raise e
    
    def get_subplot_threads(self, plot_id: int) -> List[str]:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT subplot_thread FROM BasicPlot_SubplotThread
                WHERE plot_id = %s
                """
                cursor.execute(sql, (plot_id,))
                results = cursor.fetchall()
                return [result['subplot_thread'] for result in results]
        except Exception as e:
            raise e 