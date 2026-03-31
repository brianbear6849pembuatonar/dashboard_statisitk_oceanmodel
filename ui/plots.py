import plotly.graph_objects as go
#Pengaturan plot grafik
class PlotFactory:
    @staticmethod
    def create_main_plot(layers, x_col, y_col):
        fig = go.Figure()
        
        for name, content in layers.items():
            df = content['data']
            is_raw = "Raw" in name
            
            fig.add_trace(go.Scatter(
                x=df[x_col],
                y=df[content['y']],
                name=name,
                line=dict(width=1 if is_raw else 2.5, 
                          color='gray' if is_raw else None),
                opacity=0.4 if is_raw else 1.0,
                mode='lines+markers' if "Averaging" in name else 'lines'
            ))
            
        fig.update_layout(
            template="plotly_white",
            hovermode="x unified",
            xaxis_title="Waktu (Timestamp)",
            yaxis_title=y_col,
            xaxis=dict(rangeslider=dict(visible=True))
        )
        return fig
