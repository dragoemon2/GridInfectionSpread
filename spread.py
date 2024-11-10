import numpy as np
import networkx as nx

def spread_lattice(start, m=2):
    """
    格子グラフ上の感染蔓延をシミュレートするジェネレータ関数

    Parameters
    ----------
    start : numpy.ndarray
        初期状態を表す多次元配列
    m : int
        感染者が周囲の感染者の数がこの値以上の場合に感染する
    
    Yields
    ------
    infected : numpy.ndarray
        感染者の状態を表す多次元配列

    Notes
    -----
    - 感染者は周囲の感染者がm人以上の場合に感染する
    - 感染者の状態は1, 未感染者の状態は0で表す
    - 感染者の状態は次のステップで感染が広がる
    - 感染が広がらなくなった時点でシミュレーションを終了する
    """

    infected = np.copy(start)
    while True:
        yield infected
        last_infected = np.copy(infected)
        padded = np.pad(infected, 1, 'constant', constant_values=0) # 周囲を0で埋める
        weight = np.zeros_like(padded) # 各セルの周囲の感染者数
        for i in range(padded.ndim):
            weight += np.roll(padded, 1, axis=i) + np.roll(padded, -1, axis=i) # 周囲の感染者数をカウント
        weight = weight[tuple(slice(1,-1) for i in range(padded.ndim))] # 周囲を0で埋めた部分を除去
        infected = np.where(weight >= m, 1, 0) | infected # 感染者の状態を更新
        if np.all(infected == last_infected):
            break

def spread_torus(start, m=2):
    """
    トーラス上の感染蔓延をシミュレートするジェネレータ関数

    Parameters
    ----------
    start : numpy.ndarray
        初期状態を表す多次元配列
    m : int
        感染者が周囲の感染者の数がこの値以上の場合に感染する
    
    Yields
    ------
    infected : numpy.ndarray
        感染者の状態を表す多次元配列

    Notes
    -----
    - 感染者は周囲の感染者がm人以上の場合に感染する
    - 感染者の状態は1, 未感染者の状態は0で表す
    - 感染者の状態は次のステップで感染が広がる
    - 感染が広がらなくなった時点でシミュレーションを終了する
    """

    infected = np.copy(start)
    while True:
        yield infected
        last_infected = np.copy(infected)
        weight = np.zeros_like(infected) # 各セルの周囲の感染者数
        for i in range(infected.ndim):
            weight += np.roll(infected, 1, axis=i) + np.roll(infected, -1, axis=i) # 周囲の感染者数をカウント
        infected = np.where(weight >= m, 1, 0) | infected # 感染者の状態を更新
        if np.all(infected == last_infected):
            break
        

if __name__ == '__main__':
    N = 10
    start = np.zeros((N, N, N), dtype=int)
    plane = np.eye(N, N, dtype=int)
    for i in range(N):
        start[i] = plane
        plane = np.roll(plane, 1, axis=0)
    for i, state in enumerate(spread_lattice(start)):
        print(f"Step {i}:")
        print(state)
        print()
    if np.all(state == 1):
        print("全てのセルが感染しました")
    else:
        print("感染が広がらなくなりました")