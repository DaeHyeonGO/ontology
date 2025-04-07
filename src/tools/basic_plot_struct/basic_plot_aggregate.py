from typing import List, Dict, Optional, Any, Set
from dataclasses import dataclass, field

from src.tools.basic_plot_struct.basic_plot_dao import BasicPlotDAO
from src.tools.basic_plot_struct.character_dao import CharacterDAO
from src.tools.basic_plot_struct.event_dao import EventDAO
from src.tools.basic_plot_struct.plot_point_dao import PlotPointDAO
from src.tools.basic_plot_struct.entities import BasicPlotEntity, CharacterEntity, EventEntity, PlotPointEntity

class BasicPlotAggregate:
    
    def __init__(self, host: str, user: str, password: str, database: str):
        self.basic_plot_dao = BasicPlotDAO(host, user, password, database)
        self.character_dao = CharacterDAO(host, user, password, database)
        self.event_dao = EventDAO(host, user, password, database)
        self.plot_point_dao = PlotPointDAO(host, user, password, database)
        self._plot: Optional[BasicPlotEntity] = None
    
    def create_plot(self, sequence: int, title: str, theme: str, setting: str, main_conflict: str, 
                   time_period: Optional[str] = None, resolution: Optional[str] = None) -> BasicPlotEntity:
        """새로운 기본 플롯 생성"""
        plot_id = self.basic_plot_dao.create(
            sequence=sequence,
            title=title,
            theme=theme,
            setting=setting,
            main_conflict=main_conflict,
            time_period=time_period,
            resolution=resolution
        )
        
        self._plot = BasicPlotEntity(
            id=plot_id,
            sequence=sequence,
            title=title,
            theme=theme,
            setting=setting,
            time_period=time_period,
            main_conflict=main_conflict,
            resolution=resolution
        )
        
        return self._plot
    
    def load_plot(self, plot_id: int) -> Optional[BasicPlotEntity]:
        """기존 플롯 로드 및 관련 데이터 함께 로드"""
        plot_data = self.basic_plot_dao.get_by_id(plot_id)
        if not plot_data:
            return None
        
        # 기본 플롯 데이터 로드
        self._plot = BasicPlotEntity.from_dict(plot_data)
        
        # 장르 로드
        self._plot.genres = self.basic_plot_dao.get_genres(plot_id)
        
        # 서브플롯 스레드 로드
        self._plot.subplot_threads = self.basic_plot_dao.get_subplot_threads(plot_id)
        
        # 캐릭터 로드
        character_data = self.basic_plot_dao.get_characters(plot_id)
        self._plot.characters = [CharacterEntity.from_dict(c) for c in character_data]
        
        # 플롯 포인트 로드 (이벤트 포함)
        plot_point_data = self.basic_plot_dao.get_plotpoints(plot_id)
        self._plot.plot_points = []
        
        for pp_data in plot_point_data:
            plot_point = PlotPointEntity.from_dict(pp_data)
            
            # 각 플롯 포인트의 결과 로드
            plot_point.consequences = self.plot_point_dao.get_consequences(plot_point.id)
            
            # 각 플롯 포인트의 이벤트 로드
            if plot_point.event_id:
                event_data = self.event_dao.get_by_id(plot_point.event_id)
                if event_data:
                    event = EventEntity.from_dict(event_data)
                    
                    # 이벤트의 캐릭터 로드
                    char_data = self.event_dao.get_characters(event.id)
                    event.characters = [CharacterEntity.from_dict(c) for c in char_data]
                    
                    plot_point.event = event
            
            self._plot.plot_points.append(plot_point)
        
        return self._plot
    
    def save_plot(self) -> bool:
        """플롯 저장 (업데이트)"""
        if not self._plot or not self._plot.id:
            raise ValueError("플롯이 로드되지 않았거나 새 플롯이 생성되지 않았습니다")
        
        # 기본 플롯 정보 업데이트
        result = self.basic_plot_dao.update(
            plot_id=self._plot.id,
            title=self._plot.title,
            theme=self._plot.theme,
            setting=self._plot.setting,
            time_period=self._plot.time_period,
            main_conflict=self._plot.main_conflict,
            resolution=self._plot.resolution
        )
        
        return result
    
    def delete_plot(self) -> bool:
        """플롯 삭제 (관련된 모든 데이터 함께 삭제)"""
        if not self._plot or not self._plot.id:
            raise ValueError("플롯이 로드되지 않았거나 새 플롯이 생성되지 않았습니다")
        
        result = self.basic_plot_dao.delete(self._plot.id)
        if result:
            self._plot = None
        
        return result
    
    # 장르 관련 메서드
    def add_genre(self, genre: str) -> bool:
        """장르 추가"""
        if not self._plot or not self._plot.id:
            raise ValueError("플롯이 로드되지 않았거나 새 플롯이 생성되지 않았습니다")
        
        result = self.basic_plot_dao.add_genre(self._plot.id, genre)
        if result and genre not in self._plot.genres:
            self._plot.genres.append(genre)
        
        return result
    
    def remove_genre(self, genre: str) -> bool:
        """장르 제거"""
        if not self._plot or not self._plot.id:
            raise ValueError("플롯이 로드되지 않았거나 새 플롯이 생성되지 않았습니다")
        
        result = self.basic_plot_dao.remove_genre(self._plot.id, genre)
        if result and genre in self._plot.genres:
            self._plot.genres.remove(genre)
        
        return result
    
    # 서브플롯 스레드 관련 메서드
    def add_subplot_thread(self, subplot_thread: str) -> bool:
        """서브플롯 스레드 추가"""
        if not self._plot or not self._plot.id:
            raise ValueError("플롯이 로드되지 않았거나 새 플롯이 생성되지 않았습니다")
        
        result = self.basic_plot_dao.add_subplot_thread(self._plot.id, subplot_thread)
        if result and subplot_thread not in self._plot.subplot_threads:
            self._plot.subplot_threads.append(subplot_thread)
        
        return result
    
    def remove_subplot_thread(self, subplot_thread: str) -> bool:
        """서브플롯 스레드 제거"""
        if not self._plot or not self._plot.id:
            raise ValueError("플롯이 로드되지 않았거나 새 플롯이 생성되지 않았습니다")
        
        result = self.basic_plot_dao.remove_subplot_thread(self._plot.id, subplot_thread)
        if result and subplot_thread in self._plot.subplot_threads:
            self._plot.subplot_threads.remove(subplot_thread)
        
        return result
    
    # 캐릭터 관련 메서드
    def create_character(self, name: str, role: str, description: Optional[str] = None, 
                       motivation: Optional[str] = None) -> Optional[CharacterEntity]:
        """새 캐릭터 생성"""
        character_id = self.character_dao.create(name, role, description, motivation)
        if not character_id:
            return None
        
        character = CharacterEntity(
            id=character_id,
            name=name,
            role=role,
            description=description,
            motivation=motivation
        )
        
        # 이미 플롯이 로드되어 있다면 캐릭터를 플롯에 연결
        if self._plot and self._plot.id:
            self.add_character_to_plot(character_id)
        
        return character
    
    def add_character_to_plot(self, character_id: int) -> bool:
        """플롯에 캐릭터 추가"""
        if not self._plot or not self._plot.id:
            raise ValueError("플롯이 로드되지 않았거나 새 플롯이 생성되지 않았습니다")
        
        result = self.basic_plot_dao.add_character(self._plot.id, character_id)
        
        # 캐릭터가 성공적으로 추가되었다면 메모리에 있는 캐릭터 목록도 업데이트
        if result:
            character_data = self.character_dao.get_by_id(character_id)
            if character_data:
                # 중복 추가 방지
                existing_char_ids = [c.id for c in self._plot.characters if c.id is not None]
                if character_id not in existing_char_ids:
                    self._plot.characters.append(CharacterEntity.from_dict(character_data))
        
        return result
    
    def remove_character_from_plot(self, character_id: int) -> bool:
        """플롯에서 캐릭터 제거"""
        if not self._plot or not self._plot.id:
            raise ValueError("플롯이 로드되지 않았거나 새 플롯이 생성되지 않았습니다")
        
        result = self.basic_plot_dao.remove_character(self._plot.id, character_id)
        
        # 캐릭터가 성공적으로 제거되었다면 메모리에 있는 캐릭터 목록도 업데이트
        if result:
            self._plot.characters = [c for c in self._plot.characters if c.id != character_id]
        
        return result
    
    # 이벤트 관련 메서드
    def create_event(self, title: str, description: str, importance: int = 1) -> Optional[EventEntity]:
        """새 이벤트 생성"""
        event_id = self.event_dao.create(title, description, importance)
        if not event_id:
            return None
        
        return EventEntity(
            id=event_id,
            title=title,
            description=description,
            importance=importance
        )
    
    def add_character_to_event(self, event_id: int, character_id: int) -> bool:
        """이벤트에 캐릭터 추가"""
        return self.event_dao.add_character(event_id, character_id)
    
    def remove_character_from_event(self, event_id: int, character_id: int) -> bool:
        """이벤트에서 캐릭터 제거"""
        return self.event_dao.remove_character(event_id, character_id)
    
    # 플롯 포인트 관련 메서드
    def create_plot_point(self, event_id: int, timing: str, 
                         emotional_impact: Optional[str] = None) -> Optional[PlotPointEntity]:
        """새 플롯 포인트 생성"""
        plot_point_id = self.plot_point_dao.create(event_id, timing, emotional_impact)
        if not plot_point_id:
            return None
        
        plot_point = PlotPointEntity(
            id=plot_point_id,
            event_id=event_id,
            timing=timing,
            emotional_impact=emotional_impact
        )
        
        # 이미 플롯이 로드되어 있다면 플롯 포인트를 플롯에 연결
        if self._plot and self._plot.id:
            self.add_plot_point_to_plot(plot_point_id)
        
        return plot_point
    
    def add_plot_point_to_plot(self, plot_point_id: int) -> bool:
        """플롯에 플롯 포인트 추가"""
        if not self._plot or not self._plot.id:
            raise ValueError("플롯이 로드되지 않았거나 새 플롯이 생성되지 않았습니다")
        
        result = self.basic_plot_dao.add_plotpoint(self._plot.id, plot_point_id)
        
        # 플롯 포인트가 성공적으로 추가되었다면 메모리에 있는 플롯 포인트 목록도 업데이트
        if result:
            plot_point_data = self.plot_point_dao.get_by_id(plot_point_id)
            if plot_point_data:
                plot_point = PlotPointEntity.from_dict(plot_point_data)
                
                # 결과 로드
                plot_point.consequences = self.plot_point_dao.get_consequences(plot_point_id)
                
                # 이벤트 로드
                if plot_point.event_id:
                    event_data = self.event_dao.get_by_id(plot_point.event_id)
                    if event_data:
                        event = EventEntity.from_dict(event_data)
                        char_data = self.event_dao.get_characters(event.id)
                        event.characters = [CharacterEntity.from_dict(c) for c in char_data]
                        plot_point.event = event
                
                # 중복 추가 방지
                existing_pp_ids = [pp.id for pp in self._plot.plot_points if pp.id is not None]
                if plot_point_id not in existing_pp_ids:
                    self._plot.plot_points.append(plot_point)
        
        return result
    
    def remove_plot_point_from_plot(self, plot_point_id: int) -> bool:
        """플롯에서 플롯 포인트 제거"""
        if not self._plot or not self._plot.id:
            raise ValueError("플롯이 로드되지 않았거나 새 플롯이 생성되지 않았습니다")
        
        result = self.basic_plot_dao.remove_plotpoint(self._plot.id, plot_point_id)
        
        # 플롯 포인트가 성공적으로 제거되었다면 메모리에 있는 플롯 포인트 목록도 업데이트
        if result:
            self._plot.plot_points = [pp for pp in self._plot.plot_points if pp.id != plot_point_id]
        
        return result
    
    def add_consequence_to_plot_point(self, plot_point_id: int, consequence: str) -> bool:
        """플롯 포인트에 결과 추가"""
        result = self.plot_point_dao.add_consequence(plot_point_id, consequence)
        
        # 현재 로드된 플롯에 해당 플롯 포인트가 있다면 메모리도 업데이트
        if result and self._plot:
            for pp in self._plot.plot_points:
                if pp.id == plot_point_id and consequence not in pp.consequences:
                    pp.consequences.append(consequence)
                    break
        
        return result
    
    def remove_consequence_from_plot_point(self, plot_point_id: int, consequence: str) -> bool:
        """플롯 포인트에서 결과 제거"""
        result = self.plot_point_dao.remove_consequence(plot_point_id, consequence)
        
        # 현재 로드된 플롯에 해당 플롯 포인트가 있다면 메모리도 업데이트
        if result and self._plot:
            for pp in self._plot.plot_points:
                if pp.id == plot_point_id and consequence in pp.consequences:
                    pp.consequences.remove(consequence)
                    break
        
        return result
    
    def get_current_plot(self) -> Optional[BasicPlotEntity]:
        """현재 로드된 플롯 가져오기"""
        return self._plot
