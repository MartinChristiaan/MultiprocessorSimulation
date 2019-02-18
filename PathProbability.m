N = 6;
paths = zeros(N*2,1)

for i = 1 : N*2-2
    for j = 1:min(N,N*2-1)
        paths(i+j)=paths(i+j)+1;
    end
end
