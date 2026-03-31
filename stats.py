class AnalyticsEngine:
#Pengaturan statistika
    @staticmethod
    def get_summary(series):
        return {
            "Min": round(series.min(), 3),
            "Max": round(series.max(), 3),
            "Mean": round(series.mean(), 3),
            "Std Dev": round(series.std(), 3),
            "Count": len(series)
        }