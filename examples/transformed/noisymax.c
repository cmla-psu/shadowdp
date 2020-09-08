extern void __VERIFIER_error() __attribute__ ((__noreturn__));
extern int __VERIFIER_nondet_float(void);
extern int __VERIFIER_nondet_int();
extern void __VERIFIER_assume(int);
extern void __assert_fail();
#define __VERIFIER_assert(cond) { if(!(cond)) { __assert_fail(); } }
#define Abs(x) ((x) < 0 ? -(x) : (x))
typedef enum { false = 0, true = 1 } bool;
    
int noisymax(float epsilon, int size, float q[], float __SHADOWDP_ALIGNED_DISTANCE_q[], float __SHADOWDP_SHADOW_DISTANCE_q[])
{
  __VERIFIER_assume(epsilon > 0);
  __VERIFIER_assume(size > 0);
  float __SHADOWDP_v_epsilon = 0;
  float __SHADOWDP_SHADOW_DISTANCE_max = 0;
  float __SHADOWDP_ALIGNED_DISTANCE_bq = 0;
  float __SHADOWDP_SHADOW_DISTANCE_bq = 0;
  float __SHADOWDP_ALIGNED_DISTANCE_eta = 0;
  int max = 0;
  int i = 0;
  float bq = 0;
  __SHADOWDP_SHADOW_DISTANCE_max = 0;
  __SHADOWDP_ALIGNED_DISTANCE_bq = 0;
  __SHADOWDP_SHADOW_DISTANCE_bq = 0;
  while (i < size)
  {
    __VERIFIER_assume(__SHADOWDP_ALIGNED_DISTANCE_q[i] <= 1);
    __VERIFIER_assume(__SHADOWDP_ALIGNED_DISTANCE_q[i] >= -1);
    __VERIFIER_assume(__SHADOWDP_SHADOW_DISTANCE_q[i] == __SHADOWDP_ALIGNED_DISTANCE_q[i]);
    __VERIFIER_assert(i < size);
    float eta = __VERIFIER_nondet_float();
    __SHADOWDP_v_epsilon = (((q[i] + eta) > bq) || (i == 0)) ? (0 + epsilon) : (__SHADOWDP_v_epsilon + 0);
    if (((q[i] + eta) > bq) || (i == 0))
    {
      __VERIFIER_assume(__SHADOWDP_ALIGNED_DISTANCE_q[i] <= 1);
      __VERIFIER_assume(__SHADOWDP_ALIGNED_DISTANCE_q[i] >= -1);
      __VERIFIER_assume(__SHADOWDP_SHADOW_DISTANCE_q[i] == __SHADOWDP_ALIGNED_DISTANCE_q[i]);
      __VERIFIER_assert((((q[i] + __SHADOWDP_ALIGNED_DISTANCE_q[i]) + (eta + 2)) > (bq + __SHADOWDP_SHADOW_DISTANCE_bq)) || (i == 0));
      __SHADOWDP_SHADOW_DISTANCE_max = (max + __SHADOWDP_SHADOW_DISTANCE_max) - i;
      max = i;
      __SHADOWDP_SHADOW_DISTANCE_bq = (bq + __SHADOWDP_SHADOW_DISTANCE_bq) - (q[i] + eta);
      bq = q[i] + eta;
      __SHADOWDP_ALIGNED_DISTANCE_bq = __SHADOWDP_ALIGNED_DISTANCE_q[i] + 2;
      __SHADOWDP_ALIGNED_DISTANCE_eta = 2;
    }
    else
    {
      __VERIFIER_assume(__SHADOWDP_ALIGNED_DISTANCE_q[i] <= 1);
      __VERIFIER_assume(__SHADOWDP_ALIGNED_DISTANCE_q[i] >= -1);
      __VERIFIER_assume(__SHADOWDP_SHADOW_DISTANCE_q[i] == __SHADOWDP_ALIGNED_DISTANCE_q[i]);
      __VERIFIER_assert(!(((((q[i] + __SHADOWDP_ALIGNED_DISTANCE_q[i]) + eta) > (bq + __SHADOWDP_ALIGNED_DISTANCE_bq)) || (i == 0))));
      __SHADOWDP_ALIGNED_DISTANCE_bq = __SHADOWDP_ALIGNED_DISTANCE_bq;
      __SHADOWDP_ALIGNED_DISTANCE_eta = 0;
    }

    if ((((q[i] + __SHADOWDP_SHADOW_DISTANCE_q[i]) + eta) > (bq + __SHADOWDP_SHADOW_DISTANCE_bq)) || (i == 0))
    {
      __SHADOWDP_SHADOW_DISTANCE_max = i - max;
      __SHADOWDP_SHADOW_DISTANCE_bq = ((q[i] + __SHADOWDP_SHADOW_DISTANCE_q[i]) + eta) - bq;
    }

    i = i + 1;
  }

  __VERIFIER_assert(__SHADOWDP_v_epsilon <= epsilon);
  return max;
}

