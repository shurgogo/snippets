package ds

import (
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestArraySeq(t *testing.T) {
	initList := []int{9, 8, 3, 2, 1}
	var arrayList Array[int]

	arrayList.Build(initList)
	assert.Equal(t, arrayList.Len(), len(initList))

	assert.Equal(t, arrayList.GetAt(0), initList[0])

	arrayList.SetAt(0, 5)
	assert.Equal(t, arrayList.GetAt(0), 5)

	arrayList.InsertAt(3, 10)
	assert.Equal(t, arrayList.GetAt(3), 10)
	assert.Equal(t, arrayList.Len(), len(initList)+1)

	v := arrayList.DeleteAt(3)
	assert.Equal(t, v, 10)

	arrayList.InsertFirst(60)
	assert.Equal(t, arrayList.GetAt(0), 60)
	assert.Equal(t, arrayList.Len(), len(initList)+1)
	v = arrayList.DeleteFirst()
	assert.Equal(t, v, 60)
	assert.Equal(t, arrayList.Len(), len(initList))

	arrayList.InsertLast(70)
	assert.Equal(t, arrayList.GetAt(arrayList.Len()-1), 70)
	assert.Equal(t, arrayList.Len(), len(initList)+1)
	v = arrayList.DeleteLast()
	assert.Equal(t, v, 70)
	assert.Equal(t, arrayList.Len(), len(initList))

}
