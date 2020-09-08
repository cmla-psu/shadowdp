extern void __VERIFIER_error() __attribute__ ((__noreturn__));
extern int __VERIFIER_nondet_float(void);
extern int __VERIFIER_nondet_int();
extern void __VERIFIER_assume(int);
extern void __assert_fail();
#define __VERIFIER_assert(cond) { if(!(cond)) { __assert_fail(); } }
#define Abs(x) ((x) < 0 ? -(x) : (x))
typedef enum { false = 0, true = 1 } bool;
    
int partialsum(float epsilon, int size, float q[], int __SHADOWDP_index, float __SHADOWDP_ALIGNED_DISTANCE_q[], float __SHADOWDP_SHADOW_DISTANCE_q[])
{
  __VERIFIER_assume(epsilon > 0);
  __VERIFIER_assume(size > 0);
  float __SHADOWDP_v_epsilon = 0;
  __VERIFIER_assume(__SHADOWDP_index >= 0);
  __VERIFIER_assume(__SHADOWDP_index < size);
  float __SHADOWDP_ALIGNED_DISTANCE_sum = 0;
  float out = 0;
  float sum = 0;
  int i = 0;
  __SHADOWDP_ALIGNED_DISTANCE_sum = 0;
  while (i < size)
  {
    if (i == __SHADOWDP_index)
    {
      __VERIFIER_assume(__SHADOWDP_ALIGNED_DISTANCE_q[i] <= 1);
      __VERIFIER_assume(__SHADOWDP_ALIGNED_DISTANCE_q[i] >= -1);
      __VERIFIER_assume(__SHADOWDP_SHADOW_DISTANCE_q[i] == __SHADOWDP_ALIGNED_DISTANCE_q[i]);
    }
    else
    {
      __VERIFIER_assume(__SHADOWDP_SHADOW_DISTANCE_q[i] == __SHADOWDP_ALIGNED_DISTANCE_q[i]);
      __VERIFIER_assume(__SHADOWDP_ALIGNED_DISTANCE_q[i] == 0);
    }

    __VERIFIER_assert(i < size);
    sum = sum + q[i];
    __SHADOWDP_ALIGNED_DISTANCE_sum = __SHADOWDP_ALIGNED_DISTANCE_q[i] + __SHADOWDP_ALIGNED_DISTANCE_sum;
    i = i + 1;
  }

  float eta = __VERIFIER_nondet_float();
  __VERIFIER_assert(Abs(__SHADOWDP_ALIGNED_DISTANCE_sum) <= 1);
  __SHADOWDP_v_epsilon = __SHADOWDP_v_epsilon + ((1.0 * epsilon));
  out = sum + eta;
  __VERIFIER_assert(__SHADOWDP_v_epsilon <= epsilon);
  return out;
}

