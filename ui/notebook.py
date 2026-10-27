class NotebookUI:
    def __init__(self, engine):
        self.engine = engine

    def show_collected_clues(self):
        # TODO: Oyuncunun topladığı tüm ipuçlarını göster (engine.get_collected_clues())
        pass
        
    def list_caught_contradictions(self):
        # TODO: Yakalanan çelişkileri listele (engine.get_caught_contradictions())
        pass

    def get_clue_visuals(self, clue_type):
        # TODO: İpucu türüne göre ikon ve renk ayrımı yap (physical / document / witness)
        pass

    def show_key_clue_count(self, clues):
        # TODO: Kaç anahtar ipucu toplandığını göster (is_key_clue alanı)
        pass