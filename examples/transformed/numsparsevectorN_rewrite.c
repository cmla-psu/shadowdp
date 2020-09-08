extern void __VERIFIER_error() __attribute__ ((__noreturn__));
extern int __VERIFIER_nondet_float(void);
extern int __VERIFIER_nondet_int();
extern void __VERIFIER_assume(int);
extern void __assert_fail();
#define __VERIFIER_assert(cond) { if(!(cond)) { __assert_fail(); } }
#define Abs(x) ((x) < 0 ? -(x) : (x))
typedef enum { false = 0, true = 1 } bool;
    
int numsparsevectorN(float epsilon, int size, float q[], float T, int NN, float __SHADOWDP_ALIGNED_DISTANCE_q[], float __SHADOWDP_SHADOW_DISTANCE_q[])
{
  __VERIFIER_assume(epsilon > 0);
  __VERIFIER_assume(size > 0);
  __VERIFIER_assume(NN > 0);
  float __SHADOWDP_v_epsilon = 0;
  float __SHADOWDP_ALIGNED_DISTANCE_eta_2 = 0;
  int out = 0;
  float eta_1 = __VERIFIER_nondet_float();
  __SHADOWDP_v_epsilon = __SHADOWDP_v_epsilon + (1.0 / 3.0) * epsilon;
  float T_bar = T + eta_1;
  int count = 0;
  int i = 0;
  while ((count < NN) && (i < size))
  {
    __VERIFIER_assert((count < NN) && (i < size));
    float eta_2 = __VERIFIER_nondet_float();
    __SHADOWDP_v_epsilon = (((q[i] + eta_2) >= T_bar) ? (__SHADOWDP_v_epsilon + ((1.0 / 3.0) / NN) * epsilon) : (__SHADOWDP_v_epsilon));
    if ((q[i] + eta_2) >= T_bar)
    {
      __VERIFIER_assume(__SHADOWDP_ALIGNED_DISTANCE_q[i] <= 1);
      __VERIFIER_assume(__SHADOWDP_ALIGNED_DISTANCE_q[i] >= -1);
      __VERIFIER_assume(__SHADOWDP_SHADOW_DISTANCE_q[i] == __SHADOWDP_ALIGNED_DISTANCE_q[i]);
      __VERIFIER_assert(((q[i] + __SHADOWDP_ALIGNED_DISTANCE_q[i]) + (eta_2 + 2)) >= (T_bar + 1));
      float eta_3 = __VERIFIER_nondet_float();
      __VERIFIER_assert(Abs(__SHADOWDP_ALIGNED_DISTANCE_q[i]) <= 1);
      __SHADOWDP_v_epsilon = __SHADOWDP_v_epsilon + ((1.0 / 3.0) / NN) * epsilon;
      out = q[i] + eta_3;
      count = count + 1;
      __SHADOWDP_ALIGNED_DISTANCE_eta_2 = 2;
    }
    else
    {
      __VERIFIER_assume(__SHADOWDP_ALIGNED_DISTANCE_q[i] <= 1);
      __VERIFIER_assume(__SHADOWDP_ALIGNED_DISTANCE_q[i] >= -1);
      __VERIFIER_assume(__SHADOWDP_SHADOW_DISTANCE_q[i] == __SHADOWDP_ALIGNED_DISTANCE_q[i]);
      __VERIFIER_assert(!((((q[i] + __SHADOWDP_ALIGNED_DISTANCE_q[i]) + eta_2) >= (T_bar + 1))));
      out = 0;
      __SHADOWDP_ALIGNED_DISTANCE_eta_2 = 0;
    }

    i = i + 1;
  }

  __VERIFIER_assert(__SHADOWDP_v_epsilon <= epsilon);
  return out;
}

