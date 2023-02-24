#ifndef CLASSES_H
#define CLASSES_H

struct Trip
{

};

struct Cruise
{
    int from_id;
    int to_id;
    int vehicle_id;
    int time;
    int cost;

    Cruise(int f_id, int t_id, int v_id, int t, int c)
    {
        from_id = f_id;
        to_id = t_id;
        vehicle_id = v_id;
        time = t;
        cost = c;
    }
};

#endif