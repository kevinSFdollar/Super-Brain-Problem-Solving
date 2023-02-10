# Super-Brain-Problem-Solving
Use Algorithms to Solve Puzzles in 《Super Brain》TV Show.

1.Digit_lost.py 《数字迷途》项目，将n\*n数字棋盘空缺位置补齐，使得所有数字按顺序经过所有格子并连成一条曲线，相邻两点之间可通过上下左右和对角线共8种方式连接。维护一个candidate集合，里面元素表示与当前题面上所存在数字相邻的数字。整体算法使用深度优先搜索，每次在candidate集合中取出一个元素，然后获取可放置位置，遍历有效位置进行递归求解。递归出口：candidate集合为空。

2.Number_array_lost_track.py 《数阵迷踪》项目，n\*n的数阵中相邻数字（上下左右）若存在大于1的公约数表示有边，找出数阵中一条连接所有顶点且不经过重复数字的路径。采用回溯方式对每一条边进行删除或者保留，最终返回状态为两个度为1的顶点加n*n-2个度为2的顶点，并且图中不存在回路。
