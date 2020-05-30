#include <iostream>
#include <string>
#include <algorithm>
#include <fstream>
#include <sstream>
using namespace std;

#define ques 1000000

int main()
{
    int vexNum, info;       //结点数、边信息条数
    int arcs[100][100];     //邻接矩阵
    int dist[100][100];     //经过变形Floyd算法后的信息矩阵
    string path[100][100];  //选择路径的具体路径

    int c = 0;                      // 此处更改手动测试文件，符合1-11范围的将执行单个文件，否则循环执行所有样例
    if (c >= 1 && c <= 11) {

        for (int u = 0; u < 100; u++)
            for (int v = 0; v < 100; v++) {
                arcs[u][v] = -1;
            }

        ifstream fin;
        ofstream fout;
        fin.open("../" + to_string(c) + ".txt");
        if (!fin.is_open()) {
            cout << "无法打开文件！" << endl;
            return 0;
        }
        string line;

        getline(fin, line);
        stringstream sline(line);
        sline >> vexNum >> info;

        if (vexNum > 100 || info > 1000) {cout << "顶点数必须小于等于100个，边的信息必须少于等于1000条。" << endl; return 0;}
        else if (vexNum == 0 || info == 0) {
            cout << "空无向网或无边图。" << endl;
            return -1;
        }

        for (int i = 0; i < info; i++) {
            int a, b, val;
            getline(fin, line);
            stringstream sline(line);
            sline >> a >> b >> val;
            --a; --b;
            if (a > b) {
                int temp = a;
                a = b;
                b = temp;
            }
            if (a >= vexNum || b >= vexNum || a < 0 || b < 0) {
                cout << "输入数据违规。" << endl;
                return -1;
            }
            arcs[a][b] = val;
        }

        for (int u = 0; u < vexNum; u++) {
            for (int v = u; v < vexNum; v++) {
                arcs[v][u] = arcs[u][v];
            }
            arcs[u][u] = 0;
        }

        for (int u = 0; u < vexNum; u++)
            for (int v = 0; v < vexNum; v++) {
                dist[u][v] = arcs[u][v];
                dist[v][u] = arcs[u][v];
            }

        for (int u = 0; u < vexNum; u++)
            for (int v = 0; v < vexNum; v++) {
                if (u != v && dist[u][v] >= 0)
                    path[u][v] = to_string(u + 1);
                else
                    path[u][v] = to_string(u + 1);
            }

        for (int k = 0; k < vexNum; k++)
            for (int i = 0; i < vexNum; i++)
                for (int j = 0; j < vexNum; j++) {
                    int ori = dist[i][j];
                    dist[i][j] = max(dist[i][j], min(dist[i][k], dist[k][j]));
                    dist[j][i] = dist[i][j];
                    if (i != j && i != k && k != j) {
                        if (dist[i][j] != -1 && ori < min(dist[i][k], dist[k][j])) {
                            path[i][j] = path[i][k] + " " + path[k][j];
                            path[j][i] = path[j][k] + " " + path[k][i];
                        }
                        else if (ori == min(dist[i][k], dist[k][j])) {
                            string tempathi = path[i][k] + " " + path[k][j];
                            string tempathj = path[j][k] + " " + path[k][i];
                            if (tempathi.length() < path[i][j].length() || tempathj.length() < path[j][i].length()) {
                                path[i][j] = tempathi;
                                path[j][i] = tempathj;
                            }
                            else if (tempathi.length() == path[i][j].length() || tempathj.length() == path[j][i].length()) {
                                if (path[i][j][path[i][j].length() - 1] > tempathi[tempathi.length()-1] || path[j][i][path[j][i].length() - 1] > tempathj[tempathj.length()-1]) {
                                    path[i][j] = tempathi;
                                    path[j][i] = tempathj;
                                }
                            }
                        }
                    }
                }

        for (int i = 0; i < ques; i++) {
            int a, b;
            getline(fin, line);
            stringstream sline(line);
            sline >> a >> b;
            if ((a > vexNum || b > vexNum) || a == b) {continue;}
            if (a == -1 && b == -1) {break;}
            --a; --b;
            if (dist[a][b] != -1) {
                cout << dist[a][b] << ": " << path[a][b] << " " << to_string(b + 1);
            }
            else {cout << "no path";}
            if (i != ques - 1) {cout << endl;}
        }
        fin.close();
    }
    else {                          // 进入循环执行所有11个样例
        for (c = 1; c < 12; c++)
        {
            for (int u = 0; u < 100; u++)
                for (int v = 0; v < 100; v++) {
                    arcs[u][v] = -1;
                }

            ifstream fin;
            ofstream fout;
            fin.open("../" + to_string(c) + ".txt");
            if (!fin.is_open()) {
                cout << "无法打开文件！" << endl;
                cout << endl;
                continue;
            }
            string line;

            getline(fin, line);
            stringstream sline(line);
            sline >> vexNum >> info;

            if (vexNum > 100 || info > 1000) {
                cout << "顶点数必须小于等于100个，边的信息必须少于等于1000条。" << endl;
                cout << endl;
                continue;
            }
            else if (vexNum == 0 || info == 0) {
                cout << "空无向网或无边图。" << endl;
                cout << endl;
                continue;
            }

            for (int i = 0; i < info; i++) {
                int a, b, val;
                getline(fin, line);
                stringstream sline(line);
                sline >> a >> b >> val;
                --a;
                --b;
                if (a > b) {
                    int temp = a;
                    a = b;
                    b = temp;
                }
                if (a >= vexNum || b >= vexNum || a < 0 || b < 0) {
                    cout << "输入数据违规。" << endl;
                    continue;
                }
                arcs[a][b] = val;
            }

            for (int u = 0; u < vexNum; u++) {
                for (int v = u; v < vexNum; v++) {
                    arcs[v][u] = arcs[u][v];
                }
                arcs[u][u] = 0;
            }

            for (int u = 0; u < vexNum; u++)
                for (int v = 0; v < vexNum; v++) {
                    dist[u][v] = arcs[u][v];
                    dist[v][u] = arcs[u][v];
                }

            for (int u = 0; u < vexNum; u++)
                for (int v = 0; v < vexNum; v++) {
                    if (u != v && dist[u][v] >= 0)
                        path[u][v] = to_string(u + 1);
                    else
                        path[u][v] = to_string(u + 1);
                }

            for (int k = 0; k < vexNum; k++)
                for (int i = 0; i < vexNum; i++)
                    for (int j = 0; j < vexNum; j++) {
                        int ori = dist[i][j];
                        dist[i][j] = max(dist[i][j], min(dist[i][k], dist[k][j]));
                        dist[j][i] = dist[i][j];
                        if (i != j && i != k && k != j) {
                            if (dist[i][j] != -1 && ori < min(dist[i][k], dist[k][j])) {
                                path[i][j] = path[i][k] + " " + path[k][j];
                                path[j][i] = path[j][k] + " " + path[k][i];
                            } else if (ori == min(dist[i][k], dist[k][j])) {
                                string tempathi = path[i][k] + " " + path[k][j];
                                string tempathj = path[j][k] + " " + path[k][i];
                                if (tempathi.length() < path[i][j].length() || tempathj.length() < path[j][i].length()) {
                                    path[i][j] = tempathi;
                                    path[j][i] = tempathj;
                                } else if (tempathi.length() == path[i][j].length() ||
                                           tempathj.length() == path[j][i].length()) {
                                    if (path[i][j][path[i][j].length() - 1] > tempathi[tempathi.length() - 1] ||
                                        path[j][i][path[j][i].length() - 1] > tempathj[tempathj.length() - 1]) {
                                        path[i][j] = tempathi;
                                        path[j][i] = tempathj;
                                    }
                                }
                            }
                        }
                    }

            for (int i = 0; i < ques; i++) {
                int a, b;
                getline(fin, line);
                stringstream sline(line);
                sline >> a >> b;
                if ((a > vexNum || b > vexNum) || a == b) { continue; }
                if (a == -1 && b == -1) { break; }
                --a;
                --b;
                if (dist[a][b] != -1) {
                    cout << dist[a][b] << ": " << path[a][b] << " " << to_string(b + 1);
                } else { cout << "no path"; }
                if (i != ques - 1) { cout << endl; }
            }
            fin.close();
            cout << endl;           // 回车分割样例
        }
    }
    return 0;
}