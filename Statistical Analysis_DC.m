
%pointsdata
datapoints = csvread('Points.csv');
datapoints = datapoints(1,:);
meanpoints = mean(datapoints);
npoints = length(datapoints);
 
%strokedata
datastrokes = csvread('Strokes.csv');
datastrokes = datastrokes(1,:);
meanstrokes = mean(datastrokes);
nstrokes = length(datastrokes);
 
%lillietest
[h1,p1,k1,c1] = lillietest(datapoints);
[h2,p2,k2,c2] = lillietest(datastrokes);
 
%ttest2
[h,p,ci,stats] = ttest2(datapoints,datastrokes);

%ranksum
[p,h,stats] = ranksum(datapoints,datastrokes);
 
%plots
figure, probplot(datapoints)
 
 
[f1,x1_values] = ecdf(datapoints);
F1 = figure, plot(x1_values,f1),title('pointsCDF')
 
[f2,x2_values] = ecdf(datastrokes);
F2 = figure, plot(x2_values,f2),title('strokesCDF')
 
figure,hist(datapoints),title('histogramPOINTS')
figure,hist(datastrokes),title('histogramSTROKES')


