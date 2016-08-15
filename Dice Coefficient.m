%This is a generalized implementation and might have to be tweaked to get
%the desired output
LABEL = dir('/Users/pulkit/Desktop/Dice Points Result/1/*.png'); % Ground Truth Image
SEGM = dir('/Users/pulkit/Desktop/Dice Points Result/1/*.tif'); % Segmented Image
filetobesaved = '1p.xlsx';
dicecoeff = zeros(1,numel(LABEL));
for i = 1: numel(LABEL)
    file1 = LABEL(i).name;
    set1 = imread(file1);    
    file2 = SEGM(i).name;
    set2 = imread(file2);   
    dicecoeff(i) = 2*nnz(set1 & set2)/(nnz(set1) + nnz(set2));    
end
xlswrite(filetobesaved,dicecoeff)
