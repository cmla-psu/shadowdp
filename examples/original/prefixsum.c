void prefixsum(float epsilon, int size, float q[], float T)
{
  "ONE_DIFFER;";
  "epsilon: <0, 0>; size: <0, 0>; q: <*, *>; T: <0, 0>";
  float out = 0;
  float next = 0; float n = 0; int i = 0; float sum = 0;
  while(i <= T && i < size)
  {
    float eta_1 = Lap(1.0 / epsilon, "ALIGNED; -__SHADOWDP_ALIGNED_DISTANCE_q[i];");
    next = next + q[i] + eta_1;
    sum = sum + q[i];
    out = next;
    i = i + 1;
  }
  return out;
}