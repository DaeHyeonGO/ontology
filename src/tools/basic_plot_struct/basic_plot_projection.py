from typing import List, Dict, Optional, Any, Set

from src.tools.basic_plot_struct.basic_plot_dao import BasicPlotDAO
from src.tools.basic_plot_struct.character_dao import CharacterDAO
from src.tools.basic_plot_struct.event_dao import EventDAO
from src.tools.basic_plot_struct.plot_point_dao import PlotPointDAO
from src.tools.basic_plot_struct.entities import BasicPlotEntity, CharacterEntity, EventEntity, PlotPointEntity

class BasicPlotProjection:
    """
    BasicPlotAggregate와 상반되는 읽기 전용 객체
    플롯과 관련된 데이터를 조회하는 기능만 제공
    """
    
    def __init__(self, host: str, user: str, password: str, database: str):
        self.basic_plot_dao = BasicPlotDAO(host, user, password, database)
        self.character_dao = CharacterDAO(host, user, password, database)
        self.event_dao = EventDAO(host, user, password, database)
        self.plot_point_dao = PlotPointDAO(host, user, password, database)
    
    def get_plot_by_id(self, plot_id: int) -> Optional[BasicPlotEntity]:
        """특정 ID의 플롯 조회"""
        plot_data = self.basic_plot_dao.get_by_id(plot_id)
        if not plot_data:
            return None
        
        plot = BasicPlotEntity.from_dict(plot_data)
        
        # 장르 로드
        plot.genres = self.basic_plot_dao.get_genres(plot_id)
        
        # 서브플롯 스레드 로드
        plot.subplot_threads = self.basic_plot_dao.get_subplot_threads(plot_id)
        
        return plot
    
    def get_all_plots(self) -> List[BasicPlotEntity]:
        """모든 플롯 조회"""
        plots_data = self.basic_plot_dao.get_all()
        plots = []
        
        for plot_data in plots_data:
            plot = BasicPlotEntity.from_dict(plot_data)
            # 기본 정보만 로드 (필요시 get_plot_by_id로 상세 조회)
            plots.append(plot)
        
        return plots
    
    def get_plots_by_sequence(self, sequence: int) -> List[BasicPlotEntity]:
        """특정 시퀀스의 플롯 조회"""
        plots_data = self.basic_plot_dao.get_by_sequence(sequence)
        plots = []
        
        for plot_data in plots_data:
            plot = BasicPlotEntity.from_dict(plot_data)
            plots.append(plot)
        
        return plots
    
    def get_all_sequences(self) -> List[int]:
        """모든 시퀀스 조회"""
        return self.basic_plot_dao.get_all_sequences()
    
    def get_plot_threads(self, plot_id: int) -> List[str]:
        """특정 플롯의 스레드 조회"""
        return self.basic_plot_dao.get_subplot_threads(plot_id)
    
    def get_plot_events(self, plot_id: int) -> List[EventEntity]:
        """특정 플롯의 이벤트 조회"""
        # 플롯 포인트를 통해 이벤트 ID 수집
        plot_point_data = self.basic_plot_dao.get_plotpoints(plot_id)
        events = []
        
        for pp_data in plot_point_data:
            if pp_data.get('event_id'):
                event_data = self.event_dao.get_by_id(pp_data['event_id'])
                if event_data:
                    event = EventEntity.from_dict(event_data)
                    # 이벤트 캐릭터 로드
                    char_data = self.event_dao.get_characters(event.id)
                    event.characters = [CharacterEntity.from_dict(c) for c in char_data]
                    events.append(event)
        
        return events
    
    def get_all_characters(self) -> List[CharacterEntity]:
        """모든 캐릭터 조회"""
        char_data = self.character_dao.get_all()
        return [CharacterEntity.from_dict(c) for c in char_data]
    
    def get_character_by_id(self, character_id: int) -> Optional[CharacterEntity]:
        """특정 ID의 캐릭터 조회"""
        char_data = self.character_dao.get_by_id(character_id)
        if not char_data:
            return None
        
        return CharacterEntity.from_dict(char_data)
    
    def get_plot_characters(self, plot_id: int) -> List[CharacterEntity]:
        """특정 플롯의 캐릭터 조회"""
        char_data = self.basic_plot_dao.get_characters(plot_id)
        return [CharacterEntity.from_dict(c) for c in char_data]
    
    def get_character_plots(self, character_id: int) -> List[BasicPlotEntity]:
        """특정 캐릭터가 등장하는 플롯 조회"""
        plot_ids = self.character_dao.get_related_plots(character_id)
        plots = []
        
        for plot_id in plot_ids:
            plot_data = self.basic_plot_dao.get_by_id(plot_id)
            if plot_data:
                plots.append(BasicPlotEntity.from_dict(plot_data))
        
        return plots
    
    def get_plot_points_by_plot(self, plot_id: int) -> List[PlotPointEntity]:
        """특정 플롯의 플롯 포인트 조회"""
        plot_point_data = self.basic_plot_dao.get_plotpoints(plot_id)
        plot_points = []
        
        for pp_data in plot_point_data:
            plot_point = PlotPointEntity.from_dict(pp_data)
            
            # 각 플롯 포인트의 결과 로드
            plot_point.consequences = self.plot_point_dao.get_consequences(plot_point.id)
            
            # 각 플롯 포인트의 이벤트 로드
            if plot_point.event_id:
                event_data = self.event_dao.get_by_id(plot_point.event_id)
                if event_data:
                    event = EventEntity.from_dict(event_data)
                    plot_point.event = event
            
            plot_points.append(plot_point)
        
        return plot_points
    
    def get_character_events(self, character_id: int) -> List[EventEntity]:
        """특정 캐릭터가 참여하는 이벤트 조회"""
        event_ids = self.character_dao.get_related_events(character_id)
        events = []
        
        for event_id in event_ids:
            event_data = self.event_dao.get_by_id(event_id)
            if event_data:
                events.append(EventEntity.from_dict(event_data))
        
        return events
