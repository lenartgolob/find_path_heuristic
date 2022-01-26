# Find best path with heuristic algorithms
## Rules
Find the best path from the starting field to the end with the lowest cost possible. You must capture all the treasures before arriving to the end destination. Start, treasure and end fields don't have a cost, but if the field value is >= 0, then the number is the cost of travelling through that field.

Value | Meaning 
--- | --- 
-1 | Wall
-2 | Start
-3 | Treasure
-4 | End
\>=0 | Walkable

Labyrinth example:<br/>
-1,-1,-1,-1,-1<br/>
-1,-2, 3,-3,-1<br/>
-1, 1,-1, 2,-1<br/>
-1, 5,-3, 1,-1<br/>
-1, 5,-1, 1,-1<br/>
-1,-3, 1, 1,-1<br/>
-1,-1,-1,-4,-1<br/>

## Algorithms
The problem can be saved with 4 different algorithms:
* Iterative deepening depth-first search
* Greedy best search
* A*
* IDA*

## Results
The result is a visual representation of the best path and some statistics in the console so we can see the differences between algorithms.
### Example for labyrinth_1.txt with A* algorithm
![image](https://user-images.githubusercontent.com/38143019/151164179-63a17660-60fc-4af9-82c0-7f64814b6c4a.png)

Path:
(1, 1),
(1, 2),
(1, 3),
(2, 3),
(3, 3),
(4, 3),
(5, 3),
(6, 3),
(7, 3),
(8, 3),
(9, 3),
(9, 4),
(9, 5),
(8, 5),
(7, 5),
(7, 6),
(7, 5),
(6, 5),
(5, 5),
(4, 5),
(3, 5),
(2, 5),
(1, 5),
(1, 6),
(1, 7),
(1, 8),
(1, 9),
(2, 9),
(3, 9),
(3, 8),
(3, 7),
(4, 7),
(5, 7)<br/>
Price: 112<br/>
Moves: 32<br/>
Searched nodes: 83<br/>
Used memory: 39856 bytes<br/>
Search time: 0.0010118484497070312

