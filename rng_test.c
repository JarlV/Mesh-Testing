int rng_test(int min, int max){
  int dist[5];
  int a = sizeof(dist);
  int errors = 0;
  for(int i = 0; i < sizeof(dist)/sizeof(int); i++){
    dist[i] = 0;
  }
  for(int i = 0; i < 10000; i++){
    int rn = rng(min, max);
    if(min <= rn <= max){
      dist[rn - min] += 1;
    }else{
      errors ++;
    }
  }
  return 0;
}