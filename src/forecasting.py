def simple_exponential_smoothing(sales_history, alpha=0.4):
    """Memprediksi permintaan harian berikutnya."""
    if not sales_history:
        raise ValueError("Data riwayat penjualan kosong!")
    
    forecast = sales_history[0]
    for actual in sales_history[1:]:
        forecast = alpha * actual + (1 - alpha) * forecast
    return forecast