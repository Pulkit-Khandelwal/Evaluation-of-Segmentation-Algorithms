%This is a generalized implementation and might have to be tweaked to get
%the desired output
initial = dir('/Users/pulkit/Desktop/Tanimoto Strokes/3063/*.tif');% Reference Image
segm = dir('/Users/pulkit/Desktop/Tanimoto Strokes/3063/*.tif');% All Other Images
filetobesaved = '3063st.xlsx';
Tanimoto = zeros(numel(segm),numel(segm));
for j = 1:numel(segm)
    filename = initial(j).name;
    set1 = imread(filename);
    for i = 1:numel(segm)
        filenames = segm(i).name;
        set2 = imread(filenames); 
        set2 = set2>0;
        set1 = set1>0;
        set1=set1(:);
        set2=set2(:);
        common=sum(set1 & set2); 
        union=sum(set1 | set2); 
        cGT=sum(set1); 
        cSegm=sum(set2); 
        fp=(cSegm-common);
        fn=(cGT-common);
        tp=common;
        Tanimoto(j,i) = (tp)/(tp+fp+fn);
    end
end  
xlswrite(filetobesaved,Tanimoto)
