import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

def download_stock_data(symbol='AAPL', period='1y'):
    """
    株価データをダウンロード
    
    Args:
        symbol: 株式シンボル（デフォルト: AAPL = Apple）
        period: 期間（デフォルト: 1y = 1年）
    
    Returns:
        DataFrame: 株価データ
    """
    print(f"Downloading {symbol} stock data...")
    stock = yf.Ticker(symbol)
    df = stock.history(period=period)
    
    # データをCSVに保存
    filename = f'data/{symbol}_stock_data.csv'
    df.to_csv(filename)
    print(f"Data saved to {filename}")
    
    return df


def calculate_moving_averages(df, short_window=5, long_window=20):
    """
    移動平均を計算
    
    Args:
        df: 株価データ
        short_window: 短期移動平均の期間（デフォルト: 5日）
        long_window: 長期移動平均の期間（デフォルト: 20日）
    
    Returns:
        DataFrame: 移動平均を追加したデータ
    """
    print(f"\nCalculating moving averages...")
    print(f"Short MA: {short_window} days")
    print(f"Long MA: {long_window} days")
    
    # 移動平均を計算
    df['MA_Short'] = df['Close'].rolling(window=short_window).mean()
    df['MA_Long'] = df['Close'].rolling(window=long_window).mean()
    
    return df


def plot_stock_data(df, symbol='AAPL'):
    """
    株価と移動平均をグラフ化
    
    Args:
        df: 株価データ（移動平均を含む）
        symbol: 株式シンボル
    """
    print(f"\nCreating chart for {symbol}...")
    
    plt.figure(figsize=(14, 7))
    
    # 株価をプロット
    plt.plot(df.index, df['Close'], label='Close Price', linewidth=2, color='blue')
    
    # 移動平均をプロット
    plt.plot(df.index, df['MA_Short'], label='5-Day MA', linewidth=1.5, color='orange', linestyle='--')
    plt.plot(df.index, df['MA_Long'], label='20-Day MA', linewidth=1.5, color='red', linestyle='--')
    
    # グラフの装飾
    plt.title(f'{symbol} Stock Price with Moving Averages', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Price (USD)', fontsize=12)
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # 画像として保存
    filename = f'data/{symbol}_analysis.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Chart saved to {filename}")
    
    # 表示
    plt.show()


def detect_simple_pattern(df):
    """
    簡単なパターン検出（ゴールデンクロス・デッドクロス）
    
    Args:
        df: 株価データ（移動平均を含む）
    
    Returns:
        list: 検出されたパターンのリスト
    """
    print("\nDetecting trading patterns...")
    
    patterns = []
    
    # 最新のデータを確認
    for i in range(1, min(10, len(df))):
        current = df.iloc[-i]
        previous = df.iloc[-(i+1)]
        
        # ゴールデンクロス（短期MAが長期MAを上抜け）
        if (previous['MA_Short'] < previous['MA_Long'] and 
            current['MA_Short'] > current['MA_Long']):
            patterns.append({
                'date': current.name,
                'type': 'Golden Cross',
                'price': current['Close'],
                'description': 'Buy signal: Short-term MA crossed above long-term MA'
            })
        
        # デッドクロス（短期MAが長期MAを下抜け）
        if (previous['MA_Short'] > previous['MA_Long'] and 
            current['MA_Short'] < current['MA_Long']):
            patterns.append({
                'date': current.name,
                'type': 'Dead Cross',
                'price': current['Close'],
                'description': 'Sell signal: Short-term MA crossed below long-term MA'
            })
    
    return patterns


# メイン実行
if __name__ == "__main__":
    print("=" * 60)
    print("Stock Price Analyzer")
    print("=" * 60)
    
    # ステップ1: データダウンロード
    symbol = 'AAPL'
    data = download_stock_data(symbol, '1y')
    print(f"\nDownloaded {len(data)} days of data")
    
    # ステップ2: 移動平均計算
    data = calculate_moving_averages(data, short_window=5, long_window=20)
    
    # ステップ3: パターン検出
    patterns = detect_simple_pattern(data)
    
    if patterns:
        print(f"\n🎯 Found {len(patterns)} pattern(s):")
        for pattern in patterns:
            print(f"\n  📅 Date: {pattern['date']}")
            print(f"  📊 Type: {pattern['type']}")
            print(f"  💵 Price: ${pattern['price']:.2f}")
            print(f"  📝 {pattern['description']}")
    else:
        print("\n✓ No recent patterns detected")
    
    # ステップ4: グラフ作成
    plot_stock_data(data, symbol)
    
    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60)
