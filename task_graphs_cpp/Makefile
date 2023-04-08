CXX=g++
CXX_FLAGS=-O3 -std=c++17
LIBS=-lncursesw

main: classes.cpp algorithms.cpp main.cpp
	$(CXX) $(CXX_FLAGS)  $^ $(LIBS) -o $@

clean:
	rm -f ./main